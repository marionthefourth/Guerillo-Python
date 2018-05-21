""" Search for any instances of """
import sched
import time

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
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(0, 1, self.start_stream, (scheduler,))
        scheduler.run()

    def start_stream(self, scheduler):
        if not self.main_scraper or (self.main_scraper and not self.main_scraper.busy):
            query_stream = Backend.get().database() \
                .child(Backend.get_type_folder(BackendType.QUERY)) \
                .stream(self.query_stream_handler)
            scheduler.enter(10, 1, self.start_stream, (scheduler,))
        else:
            print("Scraper busy, try again later.")

    def query_stream_handler(self, message):
        query_queue = None
        # Process new QUEUE
        if message["data"]:
            if not self.main_scraper:
                print("Searching for new queries.")
            # Check all current Queries for Requests to Complete
            for query_dict in message["data"]:
                query_without_results = Backend.get_search_queries(query_dict, with_results=False, all=False)
                if query_without_results:
                    query_queue = query_without_results
                    break
        if query_queue and query_queue.start_time:
            print("New Query To Handle:")
            print(query_queue)
            if not self.main_scraper or (self.main_scraper and not self.main_scraper.busy):
                # This code will eventually be handled by the server side
                # It is optionally done on the client-side
                self.main_scraper = Scraper.get_county_scraper(
                    query_queue,
                    FileStorage.get_full_path(Folders.EXPORTS),
                )
                if self.main_scraper:
                    # Handle Query, locking loop until it completes it
                    self.main_scraper.run()
            else:
                print("Scraper busy, try again later.")
        else:
            print("No new queries to handle.")


GuerilloServer().run()
