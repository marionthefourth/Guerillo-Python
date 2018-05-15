from guerillo.classes.backend_objects.homeowner_search_result import HomeownerSearchResult




class Scraper:

    county = None

    @staticmethod
    def get_county_scraper(county, search_query=None, exports_path=None, status_label=None):
        for county_scraper in Scraper.get_all_counties():
            if county_scraper.county.state_name == county.state_name and \
                    county_scraper.county.county_name == county.county_name:
                return county_scraper.__init__(search_query, exports_path, status_label)

    @staticmethod
    def get_all_counties():
        from guerillo.classes.scrapers.hillsborough import Hillsborough
        from guerillo.classes.scrapers.pinellas import Pinellas
        return [Pinellas(), Hillsborough()]

    def __init__(self, search_query=None, exports_path=None, status_label=None):
        from guerillo.utils.driver_utils.driver_utils import DriverUtils
        self.driver_utils = DriverUtils(exports_path=exports_path)
        self.search_result = HomeownerSearchResult(search_query)
        self.search_query = search_query
        self.status_label = status_label

    def clear_search_result(self):
        self.search_result = HomeownerSearchResult(self.search_result.query)

    def run(self):
        pass


