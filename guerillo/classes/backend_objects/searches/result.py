from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.auxiliary_object import AuxiliaryObject
from guerillo.classes.backend_objects.backend_object import BackendType
from guerillo.classes.backend_objects.searches.search import Search, SearchMode


class Result(Search):
    num_results = 0
    results_copy = None
    max_num_results = 0
    result_item_list = None
    results_reference = None
    b_type = BackendType.RESULT
    result_item_uid_list = None

    def __init__(self, uid=None, query=None, results=None, results_reference=None,
                 pyres=None, pyre=None, twin_uid=None, user_uid=None, message_data=None):
        super().__init__(uid, user_uid, twin_uid)

        if not pyres and not pyre and not message_data:
            self.result_item_list = results
            if self.result_item_list:
                self.num_results = len(self.result_item_list)
            self.query = query
            self.results_reference = results_reference
            if query:
                self.twin_uid = query.uid
                self.user_uid = query.user_uid
            self.change_mode(SearchMode.START)
        else:
            self.from_dictionary(pyres=pyres, pyre=pyre, message_data=message_data)

    def clean(self):
        if not self.is_resumed() and not self.is_done_cleaning_entries():
            self.to_next_state()
        indices_to_remove = list()
        if self.result_item_list:
            for (i, result) in enumerate(self.result_item_list):
                if result.should_remove():
                    indices_to_remove.append(i)
            for index in reversed(indices_to_remove):
                self.result_item_list.pop(index)
                self.result_item_uid_list.pop(index)
                Backend.update(self)

            self.num_results = len(self.result_item_list)
            self.to_next_state()
            return len(indices_to_remove)

        else:
            return 0

    def increase_max_num_results(self):
        self.max_num_results += 1
        Backend.update(self)

    def add(self, result_item):
        new_data = Backend.data_is_new(result_item)
        if new_data[0]:
            Backend.save(result_item)
        else:
            result_item.uid = new_data[1]

        if not self.result_item_list:
            self.result_item_list = list()

        if not self.result_item_uid_list:
            self.result_item_uid_list = list()

        self.result_item_list.append(result_item)
        self.num_results = len(self.result_item_list)
        self.result_item_uid_list.append(result_item.uid)
        Backend.update(self)

    def remove(self, result_item):
        if not self.result_item_list:
            self.result_item_list = list()

        if not self.result_item_uid_list:
            self.result_item_uid_list = list()

        self.result_item_list.remove(result_item)
        self.num_results = len(self.result_item_list)
        Backend.update(self)

    def from_dictionary(self, pyres=None, pyre=None, message_data=None):
        dictionary = super().from_dictionary(pyres=pyres, pyre=pyre, message_data=message_data)
        if dictionary:
            self.num_results = dictionary.get("num_results", 0)
            self.max_num_results = dictionary.get("max_num_results", 0)
            self.results_reference = dictionary.get("results_reference", None)
            self.result_item_uid_list = AuxiliaryObject.get_uid_list_from_dictionary(self, dictionary, v_index=1)
        return dictionary

    def to_dictionary(self):
        main_dict = {
            **super().to_dictionary(),
            "num_results": self.num_results,
            "max_num_results": self.max_num_results,
            "results_reference": self.results_reference
        }
        if self.result_item_uid_list:
            return {
                    ** main_dict,
                    ** AuxiliaryObject.get_uid_dictionary_from_uid_list(self, self.result_item_uid_list, v_index=1)
            }
        else:
            return main_dict

    def to_list(self):
        result_list = list()
        result_list.append(["Name", "Address", "Date/Time", "Amount of Mortgage", "Property Sale Price"])
        for homeowner in self.result_item_list:
            result_list.append(homeowner.to_list())

        header_row = result_list.pop(0)
        result_list.sort(key=lambda x: float(x[3]), reverse=True)
        result_list.insert(0, header_row)

        return result_list
