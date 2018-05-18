from guerillo.backend.backend import Backend
from guerillo.classes.backend_objects.backend_object import BackendType
from guerillo.classes.backend_objects.search.result import Result
from guerillo.utils.sanitizer import Sanitizer


class Scraper(object):
    county = None

    @staticmethod
    def get_county_scraper(search_query=None, exports_path=None):
        for county_scraper in Scraper.get_all_counties():
            for county_uid in search_query.county_uid_list:
                county = Backend.read(BackendType.COUNTY, uid=county_uid)
                if county_scraper.__name__ == Sanitizer.county_name(county.county_name) + county.state_name:
                    return county_scraper(search_query, exports_path)

    @staticmethod
    def get_all_counties():
        # TODO - Dynamically Pull All County Scrapers
        # return [cls.__name__ for cls in Scraper.__subclasses__()]
        from guerillo.classes.scrapers.florida.pinellas_fl import PinellasFL
        from guerillo.classes.scrapers.florida.hillsborough_fl import HillsboroughFL
        return [PinellasFL, HillsboroughFL]

    def __init__(self, search_query=None, exports_path=None):
        from guerillo.utils.driver_utils.driver_utils import DriverUtils
        self.driver_utils = DriverUtils(exports_path=exports_path)
        self.search_result = Result(uid=search_query.twin_uid, query=search_query)
        self.search_query = search_query

    def clear_search_result(self):
        self.search_result = Result(self.search_result.query)

    def run(self):
        pass
