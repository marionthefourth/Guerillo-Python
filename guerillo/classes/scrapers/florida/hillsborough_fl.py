# -*- coding: utf-8 -*-
"""
Created on Tue May  1 00:11:23 2018

@author: Kenneth
"""
from datetime import datetime

from guerillo.classes.backend_objects.county import County
from guerillo.classes.scrapers.scraper import Scraper
from guerillo.config import HTML, URLs, General
from guerillo.utils.driver_utils.actions.action import ActionType, Target
from guerillo.utils.driver_utils.actions.action_click import ActionClick
from guerillo.utils.driver_utils.actions.action_complex import ActionComplex
from guerillo.utils.driver_utils.actions.action_find import ActionFind
from guerillo.utils.driver_utils.actions.action_get import ActionGet
from guerillo.utils.driver_utils.actions.action_return import ActionReturn
from guerillo.utils.driver_utils.actions.action_wait import ActionWait

"""
https://hillsborough.county-taxes.com/public/real_estate/parcels/A1653890000
165389-0000
so far all folio formats for tax est are the above^ reformatted
A1653890000
so "A"+folio_string.replace("-","")

"""


class HillsboroughFL(Scraper):
    """Property Appraiser Traverse & Scrape Logic"""
    county = County(state_name="FL", county_name="Hillsborough County")

    def property_appraiser_scrape_r(self, name):
        self.driver_utils.process(actions=[
            ActionGet(target=URLs.HCPAFL.OWNER + name + HTML.PAGE_SIZE_80),
            ActionComplex(actions=[
                ActionFind(ActionType.FIND_ID, target=General.HCPAFL.TABLE_RESULTS),
                ActionFind(ActionType.FIND_TAGS_BY_NAME, primary_target=Target.PREVIOUS_RESULT, target=HTML.TR),
                ActionFind(ActionType.FIND_TAGS_BY_NAME, primary_target=Target.PREVIOUS_RESULT, target=HTML.TD),
                ActionReturn()
            ])
        ])

    def property_appraiser_scrape(self):
        name_string = "SMITH JACK L"
        name_to_search = name_string.split(" ")[0] + ", " + name_string.split(" ")[1]
        # this example should be "SMITH, JACK"
        self.driver_utils.driver.get(URLs.HCPAFL.OWNER + name_to_search + HTML.PAGE_SIZE_80)
        table = self.driver_utils.driver.find_element_by_id(General.HCPAFL.TABLE_RESULTS)
        table_tr_tags = table.find_elements_by_tag_name(HTML.TR)
        cleaned_rows = []
        for tr_tag in table_tr_tags:
            td_tags = tr_tag.find_elements_by_tag_name(HTML.TD)
            cleaned_row = []
            for td_tag in td_tags:
                cleaned_row.append(td_tag.text)
            cleaned_rows.append(cleaned_row)
        print(cleaned_rows)
        """ Enumed::: information header -> index: """
        FOLIO = 0
        NAME = 1
        STREET_ADDRESS = 2
        SALE_DATE = 3
        CONSIDERATION = 4
        HOMESTEAD = 5
        """"""

        # this javascript you can just click the row WebElement as a whole:
        ###EXAMPLE:
        table_tr_tags[2].click()
        ### after clicking, then this logic (dynamc, not just example anymore):
        legal_description = ""
        body_tags = self.driver_utils.driver.find_elements_by_tag_name(HTML.T_BODY)
        for body_tag in body_tags:
            if body_tag.get_attribute(HTML.DATA_BIND) == "foreach: fullLegal()":
                legal_description = body_tag.text

    def get_search_query_url(self):
        return URLs.HillsboroughClerk.SEARCH + \
               URLs.HillsboroughClerk.BEGIN_DATE + self.search_query.start_date + \
               URLs.HillsboroughClerk.END_DATE + self.search_query.end_date + \
               URLs.HillsboroughClerk.LOWER_BOUND + self.search_query.lower_bound + \
               URLs.HillsboroughClerk.UPPER_BOUND + self.search_query.upper_bound + \
               URLs.HillsboroughClerk.CONSIDERATION

    def get_deeds_r(self):
        self.driver_utils.process(actions=[
            ActionGet(target=self.get_search_query_url()),
            ActionWait(ActionType.WAIT_FOR_ID, target=General.HCPAFL.HL_SETTINGS),
            ActionFind(ActionType.FIND_ID, target=General.HCPAFL.HL_SETTINGS),
            ActionClick(primary_target=Target.PREVIOUS_RESULT)
        ])

    def get_deeds(self):

        lower_bound = "200000"
        upper_bound = "600000"
        start_date = "04/01/2018"
        end_date = "04/03/2018"
        today_date = datetime.today().strftime("%m/%d/%Y")

        url_string = "https://pubrec3.hillsclerk.com/oncore/search.aspx?bd=" + start_date + "&ed=" + end_date + "&bt=O&lb=" + lower_bound + "&ub=" + upper_bound + "&pt=-1&dt=MTG&st=consideration"
        self.driver_utils.driver.get(url_string)
        # doing the straight to URL method saves a little bit of pain
        # however we want to maximize the search results. we have to click a 'setings' link
        # then handle the fact that it pops up in a new window.
        # the below chunk handles clicking that link and focusing the popup
        main_window_handle = None
        while not main_window_handle:
            main_window_handle = self.driver_utils.driver.current_window_handle
            self.driver_utils.driver.find_element_by_id("PageHeader1_hlSettings").click()
        settings_window_handle = None
        while not settings_window_handle:
            for handle in self.driver_utils.driver.window_handles:
                if handle != main_window_handle:
                    settings_window_handle = handle
                    break
        self.driver_utils.driver.switch_to.window(settings_window_handle)
        # now we just need to manipulate the results count and submit
        self.driver_utils.driver.find_element_by_id("cboResultCount").send_keys("500")
        self.driver_utils.driver.find_element_by_id("cmdSubmit").click()
        # that window doesn't exist but our driver is still focused on it
        # we need to focus back. we already saved main_handle as a variable
        # so we can just use that
        self.driver_utils.driver.switch_to.window(main_window_handle)
        # now that we're back, we'll have to reload the search
        # given potential speed issues, but the fact that we can't wait for id
        # (beacuse the ids of what we want are already there, we just don't have
        # all the results displayed in chunks of 500, but instead 30)
        # so we'll do an all encompassing check:
        stale_page = self.driver_utils.driver.page_source
        self.driver_utils.driver.find_element_by_id("cmdSubmit").click()
        while self.driver_utils.driver.page_source == stale_page:
            pass
        # we should be good now, so on to table shenanigans
        # TODO: check if using bs4 to parse is faster. PROBABLY IS THO

        table = self.driver_utils.driver.find_element_by_id("dgResults")
        table_rows = table.find_elements_by_tag_name("tr")
        data_results = ["Mortgage Amount", "Full Name", "Counterparty Name", "Date", "Legal Description"]
        for row in table_rows:
            rc = row.find_elements_by_tag_name("td")  # rc = row_columns
            if len(rc) >= 12:
                data_results.append(
                    rc[2].text, rc[3].text, rc[4].text, rc[5].text, rc[10].text
                )

        print(data_results)
        """
        Columns by Header
        0: Result/Row#
        1: Status (????)
        2: Mortgage Amount
        3: Full Name
        4: Counterparty Name
        5: Date
        6: Document Type
        7: Book (O = official record)
        8: Book #
        9: Page #
        10: Legal Desc
        11: Instrument #

        Only really need 3,4,5,6,11
        """
        # TODO: handle max limit of 2000 searchs (hills may need to be limited)
        # TODO: maybe just search mortgages, then look for that deed through more queries
        # TODO: pull legal, do a single search with legal sec
        # TODO: the full name from the mortgage will be the counterparty, so verify all entries
        # TODO: to have that. THen make sure the doctype is a deed
        # TODO: if over 3 weeks old, start by just looking for full name in HCAPFL first
        # TODO: if that can' find it, then scour the counterparty and search that way
        # TODO: for anything newer than 3 weeks, same process but vice-versa

    def run(self):
        pass