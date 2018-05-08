from guerillo.utils.driver_utils.driver_utils import DriverUtils
from guerillo.classes.backend_objects.homeowner_search_result import HomeownerSearchResult


class Scraper:

    def __init__(self, search_query=None, exports_path=None):
        self.driver_utils = DriverUtils(exports_path=exports_path)
        self.search_result = HomeownerSearchResult(search_query)
        self.search_query = search_query

    def clear_search_result(self):
        self.search_result = HomeownerSearchResult(self.search_result.query)

    def run(self):
        pass


