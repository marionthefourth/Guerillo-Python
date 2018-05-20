""" Search for any instances of """
from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.backend_object import BackendType
from guerillo.classes.scrapers.scraper import Scraper
from guerillo.config import Folders
from guerillo.utils.file_storage import FileStorage


class GuerilloServer:
    query_queue = list()
    main_scraper: Scraper

    def run(self):

        self.main_scraper = None
        # Check all current Queries for Requests to Complete
        # query_queue = Backend.get_search_queries(with_results=False)

        # Handle Query, locking loop until it completes it
        # while(query_queue):

        query_stream = Backend.get().database() \
            .child(Backend.get_type_folder(BackendType.QUERY)) \
            .stream(self.query_stream_handler)

    def query_stream_handler(self, message):
        print(message["data"])

        # Process new QUEUE
        if message["data"]:
            for query_dict in message["data"]:
                query_without_results = Backend.get_search_queries(query_dict, with_results=False, all=False)
                if query_without_results:
                    for query in self.query_queue:
                        if query_without_results.uid == query.uid:
                            continue
                    self.query_queue.append(query_without_results)
            pass

        print(self.query_queue)
        if len(self.query_queue) >= 1:
            if not self.main_scraper:
                # This code will eventually be handled by the server side
                # It is optionally done on the client-side
                self.main_scraper = Scraper.get_county_scraper(
                    self.query_queue.pop(0),
                    FileStorage.get_full_path(Folders.EXPORTS),
                )
            if self.main_scraper and not self.main_scraper.busy:
                self.main_scraper.run()
