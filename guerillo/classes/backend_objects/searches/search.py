from datetime import datetime
from enum import IntEnum, Enum

from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.backend_object import BackendObject, BackendType


class SearchState(IntEnum):
    DEFAULT = 100
    NUMBERING_RESULTS = 200
    SEARCH_BY_BOOKPAGE = 300
    SEARCH_BY_NAME = 400
    ENTRY_CLEANING = 500

    @staticmethod
    def get_all_types():
        return [
            SearchState.NUMBERING_RESULTS,
            SearchState.SEARCH_BY_BOOKPAGE,
            SearchState.SEARCH_BY_NAME,
            SearchState.ENTRY_CLEANING,
        ]

    @staticmethod
    def from_string(string_type):
        for s_state in SearchState.get_all_types():
            if string_type == s_state.name:
                return s_state
        return SearchState.DEFAULT


class SearchType(Enum):
    PARCEL = "Parcel"
    DEFAULT = "Default"
    DOCUMENT = "Document"
    HOMEOWNER = "Homeowner"

    @staticmethod
    def get_all_types():
        return [SearchType.PARCEL, SearchType.DOCUMENT, SearchType.HOMEOWNER, SearchType.DEFAULT]

    @staticmethod
    def from_string(string_type):
        for s_type in SearchType.get_all_types():
            if string_type == s_type.name:
                return s_type
        return SearchType.DEFAULT


class SearchMode(IntEnum):
    DONE = 600
    STOP = 500
    START = 100
    STARTED = 150
    PAUSE = 200
    PAUSED = 250
    RESUME = 300
    RESUMED = 350
    UPDATE = 700
    UPDATING = 733
    UPDATED = 767
    DEFAULT = 800

    @staticmethod
    def get_all_types():
        return [
            SearchMode.DONE,
            SearchMode.STOP,
            SearchMode.START,
            SearchMode.STARTED,
            SearchMode.PAUSE,
            SearchMode.PAUSED,
            SearchMode.RESUME,
            SearchMode.RESUMED,
            SearchMode.UPDATE,
            SearchMode.UPDATING,
            SearchMode.UPDATED,
            SearchMode.DEFAULT
        ]

    @staticmethod
    def from_string(string_type):
        for s_mode in SearchMode.get_all_types():
            if string_type == s_mode.name:
                return s_mode
        return SearchMode.DEFAULT


class Search(BackendObject):
    twin_uid = None
    end_time = None
    start_time = None
    b_type = BackendType.SEARCH

    def __init__(self, uid=None, user_uid=None, twin_uid=None):
        super().__init__(uid)
        self.user_uid = user_uid
        if self.b_type == BackendType.QUERY:
            self.twin_uid = Backend.generate_uid() if not twin_uid else twin_uid
        else:
            self.twin_uid = twin_uid

        self.s_mode = SearchMode.DEFAULT
        self.s_state = SearchState.DEFAULT
        self.s_type = SearchType.HOMEOWNER

    def from_dictionary(self, pyres=None, pyre=None, message_data=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre, message_data=message_data)
        if dictionary:
            self.user_uid = dictionary.get("user_uid", None)
            self.end_time = dictionary.get("end_time", None)
            self.start_time = dictionary.get("start_time", None)
            self.twin_uid = dictionary.get(self.get_twin_key(), None)
            self.s_type = SearchType.from_string(dictionary.get("search_type", None))
            self.s_mode = SearchMode.from_string(dictionary.get("search_mode", None))
            self.s_state = SearchState.from_string(dictionary.get("search_state", None))
        return dictionary

    def get_twin_key(self):
        return "result_uid" if self.b_type == BackendType.QUERY else "query_uid"

    def to_dictionary(self):
        main_dict = {
            **super().to_dictionary(),
            "user_uid": self.user_uid,
            "search_type": self.s_type.name,
            "search_mode": self.s_mode.name,
            "search_state": self.s_state.name,
            self.get_twin_key(): self.twin_uid
        }
        if self.start_time:
            main_dict["start_time"] = str(self.start_time)

        if self.end_time:
            main_dict["end_time"] = str(self.end_time)

        return main_dict

    def change_mode(self, s_mode):
        self.s_mode = s_mode

        if s_mode == SearchMode.START:
            self.start()
            return
        elif s_mode == SearchMode.DONE:
            self.finish()
        elif s_mode == SearchMode.STOP:
            self.stop()
        elif s_mode == SearchMode.PAUSE:
            self.pause()
        elif s_mode == SearchMode.UPDATE:
            self.update()
        elif s_mode == SearchMode.RESUME:
            self.resume()

        Backend.update(self)

    def is_done_numbering_results(self):
        return self.s_state.value > SearchState.NUMBERING_RESULTS.value

    def is_done_searching_by_bookpage(self):
        return self.s_state.value > SearchState.SEARCH_BY_BOOKPAGE.value

    def is_done_searching_by_name(self):
        return self.s_state.value > SearchState.SEARCH_BY_NAME.value

    def is_done_cleaning_entries(self):
        return self.s_state.value > SearchState.ENTRY_CLEANING.value

    def start(self):
        self.start_time = datetime.now()
        Backend.save(self)

    def is_stopped(self):
        return self.s_mode == SearchMode.STOP

    def stop(self):
        self.s_mode = SearchMode.STOP
        # self.stopped_time = datetime.now()
        Backend.update(self)

    def is_paused(self):
        return self.s_mode == SearchMode.PAUSE

    def pause(self):
        self.s_mode = SearchMode.PAUSE

        # self.paused_time = datetime.now()
        Backend.update(self)

    def is_resumed(self):
        return self.s_mode == SearchMode.RESUMED

    def resume(self):
        self.s_mode = SearchMode.RESUME
        Backend.update(self)

    def is_updating(self):
        return self.s_mode == SearchMode.UPDATING

    def update(self):
        self.s_mode = SearchMode.UPDATE
        Backend.update(self)

    def transcend_state(self):
        if self.s_mode == SearchMode.START:
            return

    def to_next_state(self):
        if not self.is_paused() or not self.is_stopped():
            if self.s_state == SearchState.DEFAULT:
                self.s_state = SearchState.NUMBERING_RESULTS
            elif self.s_state == SearchState.NUMBERING_RESULTS:
                self.s_state = SearchState.SEARCH_BY_BOOKPAGE
            elif self.s_state == SearchState.SEARCH_BY_BOOKPAGE:
                self.s_state = SearchState.SEARCH_BY_NAME
            elif self.s_state == SearchState.SEARCH_BY_NAME:
                self.s_state = SearchState.ENTRY_CLEANING
            elif self.s_state == SearchState.ENTRY_CLEANING:
                self.s_state = SearchState.DEFAULT
                self.change_mode(SearchMode.DONE)

    def is_done(self):
        return self.s_mode == SearchMode.DONE

    def finish(self):
        self.end_time = datetime.now()
