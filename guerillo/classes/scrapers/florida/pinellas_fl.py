# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:14:10 2018

@author: Panoramic, Co.
"""
from datetime import datetime

import bs4
from selenium.webdriver.common.keys import Keys

from guerillo.classes.backend_objects.county import County
from guerillo.classes.backend_objects.result_items.homeowner import Homeowner
from guerillo.classes.scrapers.scraper import Scraper
from guerillo.config import URLs, General, HTML, Folders, KeyFiles
from guerillo.utils.driver_utils.actions.action import Operation, ActionType
from guerillo.utils.driver_utils.actions.action_clear import ActionClear
from guerillo.utils.driver_utils.actions.action_click import ActionClick
from guerillo.utils.driver_utils.actions.action_complex import ActionComplex
from guerillo.utils.driver_utils.actions.action_find import ActionFind
from guerillo.utils.driver_utils.actions.action_get import ActionGet
from guerillo.utils.driver_utils.actions.action_match_text import ActionMatchText
from guerillo.utils.driver_utils.actions.action_repeat import ActionRepeat, Loop
from guerillo.utils.driver_utils.actions.action_return import ActionReturn, Condition
from guerillo.utils.driver_utils.actions.action_send_keys import ActionSendKeys
from guerillo.utils.driver_utils.actions.action_wait import ActionWait
from guerillo.utils.file_storage import FileStorage
from guerillo.utils.sanitizer import Sanitizer


class PinellasFL(Scraper):
    county = County(state_name="FL", county_name="Pinellas County")

    def search_by_bookpage(self, bookpage):
        self.driver_utils.process(actions=[
            ActionGet(target=URLs.PCPAO.SEARCH_BY_OR),
            ActionSendKeys(ActionType.SEND_KEYS_BY_TAG, Operation(General.BUTTON, Keys.SPACE)),  # Accept Disclaimer
            ActionWait(ActionType.WAIT_FOR_ID, target=General.TEXT_1),
            ActionSendKeys(ActionType.SEND_KEYS_BY_ID, Operation(General.TEXT_1, bookpage)),
            ActionSendKeys(ActionType.SEND_KEYS_BY_NAME, Operation(General.PCPAO.BUTTON_SUBMIT, Keys.SPACE)),
            ActionWait(ActionType.WAIT_FOR_ID, target=General.LINK_BAR),
        ])

    def get_site_address(self, url):
        return self.driver_utils.process(actions=[
            ActionGet(target=url),
            ActionComplex([  # Should be @ Tax Accessor
                ActionFind(ActionType.FIND_TAGS_BY_NAME, target=General.BUTTON),
                ActionMatchText(value=General.I_AGREE),
                ActionSendKeys(value=Keys.SPACE)
            ]),
            ActionWait(ActionType.WAIT_FOR_ID, target=General.PCPAO.ADDR_NS),
            ActionReturn(operations=[
                Operation(sub_action=ActionType.FIND_ID, target=General.PCPAO.ADDR_NS),
                Operation(sub_action=ActionType.GET_ATTRIBUTE, target=General.VALUE)
            ])
        ])

    def should_continue_search(self, name):
        return self.driver_utils.process(
            ActionComplex(actions=[
                ActionFind(ActionType.FIND_ID, target=General.PCPAO.ITB),
                ActionFind(ActionType.FIND_TAGS_BY_NAME, target=HTML.TD),
                ActionMatchText(target=General.PCPAO.NO_RECORDS),
                ActionGet(target=URLs.PCPAO.TEXT_1 + Sanitizer.general_name(name) + HTML.NUM_RESULTS_1000),
                ActionRepeat(loops=[
                    Loop(ActionType.FIND_ID, ActionType.GET),
                    Loop(ActionType.FIND_ID, ActionType.MATCH_TEXT)
                ]),
                ActionReturn(operations=[
                    Operation(target=Condition.MATCH_FAIL, value=True),
                    Operation(target=Condition.REPEAT_COMPLETION, value=False),
                ])
            ])
        )

    def fill_search_query_fields(self):
        self.search_query.sanitize()
        self.driver_utils.process(
            ActionClear(ActionType.CLEAR_THEN_SEND, operations=[
                Operation(General.PCPAO.RECORD_FROM, self.search_query.start_date),
                Operation(General.PCPAO.RECORD_TO, self.search_query.end_date),
                Operation(General.PCPAO.LOWER_BOUND, self.search_query.lower_bound),
                Operation(General.PCPAO.UPPER_BOUND, self.search_query.upper_bound)
            ])
        )
        self.search_query.desanitize()

    def accept_terms_and_conditions(self):
        self.driver_utils.process(actions=[
            ActionGet(target=URLs.MyPinellasClerk.SEARCH_TYPE_CONSIDERATION),
            ActionClick(target=General.PCPAO.BUTTON)  # Hit Accept Terms Button
        ])

    def get_search_result_count_by_name(self, name):
        try:
            header = self.driver_utils.process(actions=[
                ActionGet(target=URLs.PCPAO.TEXT_1 + name + HTML.NUM_RESULTS_1000),
                ActionReturn(operation=Operation(value=ActionType.FIND_TAG_NAME, target=HTML.TH))
            ])
        except AttributeError:
            return 0

        return int(header.text.split("through ")[1].split(" of")[0])

    def download_csv_file(self):
        self.driver_utils.process(actions=[
            ActionClick(target=General.PCPAO.BUTTON_SEARCH),
            ActionWait(ActionType.WAIT_FOR_CLASS, target=HTML.T_GRID_CONTENT),
            ActionWait(ActionType.WAIT_FOR_CLASS_EXCEPTION, target=HTML.T_NO_DATA),
            ActionClick(target=General.PCPAO.BUTTON_CSV)
        ])

        downloaded_file_name = FileStorage.get_full_path(Folders.EXPORTS) + KeyFiles.SEARCH_RESULTS
        FileStorage.handle_timeout(self.driver_utils.driver, downloaded_file_name)  # Wait For Download
        return self.rename_downloaded_csv_file(downloaded_file_name)

    def create_deeds_and_mortgages_list(self, file_name):
        data_lists = FileStorage.read(file_name, county_filter=self.county.county_name)
        deeds = list()
        mortgages = list()
        if data_lists:
            for item in data_lists:
                if item[0] != "" and item[1] != "" and item[6] != "":
                    if item[3] == General.DEED:
                        deeds.append(item)
                    elif item[3] == General.MORTGAGE:
                        mortgages.append(item)
            return deeds, mortgages
        raise FileNotFoundError

    def create_bookpage_list(self, deeds_list, mortgages_list):
        #  Check Mortgages for Leads
        #  Get Deed Bookpages
        homeowners = list()
        for mortgage in mortgages_list:
            if mortgage[0] != "":  # Check if Mortgage has a name
                for deed in deeds_list:
                    if mortgage[0] == deed[1]:  # Check Mortgage Entry Name to find Deed Item
                        homeowners.append(Homeowner(mortgage_item=mortgage, deed_item=deed))
                        if self.search_result.is_resumed() and len(homeowners) <= self.search_result.num_results:
                            continue
                        self.search_result.increase_max_num_results()

        self.search_result.results_copy = homeowners

    def create_report_list(self):
        if not self.search_result.is_done_numbering_results():
            self.scrape_number_of_results()
        elif self.search_result.is_resumed():
            self.recreate_bookpage_list()

        if not self.search_result.is_done_searching_by_bookpage():
            self.scrape_by_bookpage()
        if not self.search_result.is_done_searching_by_name():
            self.scrape_by_name()
        if not self.search_result.is_done_cleaning_entries():
            self.search_result.clean()

    def scrape_number_of_results(self):
        if not self.search_result.is_resumed() and not self.search_result.is_done_numbering_results():
            self.search_result.to_next_state()

        if not self.search_result.results_reference:
            self.accept_terms_and_conditions()
            self.fill_search_query_fields()  # Data Ranges Entry
            downloaded_file_name = self.download_csv_file()  # Download CSV file provided and rename it
            self.search_result.results_reference = downloaded_file_name
            from guerillo.backend.backend import Backend
            Backend.update(self.search_result)
        else:
            downloaded_file_name = self.search_result.results_reference

        deeds_and_mortgages = self.create_deeds_and_mortgages_list(downloaded_file_name)
        self.create_bookpage_list(deeds_and_mortgages[0], deeds_and_mortgages[1])

    def scrape_by_bookpage(self):
        if not self.search_result.is_resumed() and not self.search_result.is_done_searching_by_bookpage():
            self.search_result.to_next_state()
        for (i, homeowner) in enumerate(self.search_result.results_copy):
            if self.search_result.is_resumed() and i + 1 <= self.search_result.num_results:
                continue
            self.search_by_bookpage(homeowner.bookpage)
            # Get the link (hardcoded because always one result)
            addresses = self.driver_utils.driver.find_element_by_id(General.PCPAO.ITB).find_elements_by_tag_name(HTML.A)
            if len(addresses) != 0:
                address = self.get_site_address(
                    addresses[1].get_attribute(HTML.HREF).replace("general", General.PCPAO.TAX_EST))
                homeowner.address = address

                self.search_result.add(homeowner)

    def scrape_by_name(self):
        if not self.search_result.is_resumed() and not self.search_result.is_done_searching_by_name():
            self.search_result.to_next_state()
        for (i, homeowner) in enumerate(self.search_result.results_copy):
            if self.search_result.is_resumed() and i + 1 <= self.search_result.num_results:
                continue
            if not homeowner.address:
                if self.get_search_result_count_by_name(homeowner.counterparty_name) <= 50:
                    if self.should_continue_search(homeowner.counterparty_name):
                        match_with_line = self.find_subdivision_match(homeowner)
                        if match_with_line[0]:
                            url = URLs.PCPAO.HOME + match_with_line[1][1].replace("general", General.PCPAO.TAX_EST)
                            homeowner.address = self.get_site_address(url)

                            self.search_result.add(homeowner)

    def find_subdivision_match(self, homeowner):
        # Check for Results Again
        itb = self.driver_utils.driver.find_element_by_id(General.PCPAO.ITB)  # main table with data

        soup = bs4.BeautifulSoup(itb.get_attribute(HTML.OUTER), HTML.PARSER)
        rows = soup.find_all(HTML.TR)
        # now, row[*].find_all('td') returns a list that has each item comma delimited
        # [5] = Subdivision (which our legal description can look against)
        # [1] = Link for Parcel
        sub_and_link = []  # let's just make a list of the results to parse through first
        for row in rows:
            row_list = row.find_all(HTML.TD)
            if len(row_list) >= 6:
                sub_and_link.append([row_list[5].text, row_list[1].a[HTML.HREF]])
        # Use list to traverse legal description vs subdivision name
        for line in sub_and_link:
            match_count = 0  # Count number of word matches (order unimportant)
            # 2 or more matches should signify a hit
            subdivision_searchable = line[0].split(" ")  # line[0] = subdivision name
            for term in homeowner.legal_description.split(" "):  # Input List w/ space delimited legal description.
                for compared_term in subdivision_searchable:
                    if term == compared_term:
                        match_count += 1
                if match_count >= 2:
                    break
            if match_count >= 2:
                return True, line

        return False, None

    def rename_downloaded_csv_file(self, file_name):
        export_path = FileStorage.get_full_path(Folders.EXPORTS)

        end_date = Sanitizer.date(self.search_query.end_date)
        start_date = Sanitizer.date(self.search_query.start_date)
        self.search_query.sanitize()
        lower_bound = self.search_query.lower_bound
        upper_bound = self.search_query.upper_bound
        self.search_query.desanitize()
        current_date_time = Sanitizer.date_time(str(datetime.now()))

        renamed_downloaded_file_name = export_path + start_date + "-" + end_date + " " + lower_bound + " " + upper_bound + " " + current_date_time + ".csv"

        FileStorage.rename(file_name, renamed_downloaded_file_name)
        return renamed_downloaded_file_name

    def recreate_bookpage_list(self):
        if self.search_result.results_reference:
            deeds_and_mortgages = self.create_deeds_and_mortgages_list(self.search_result.results_reference)
            self.create_bookpage_list(deeds_and_mortgages[0], deeds_and_mortgages[1])
        else:
            self.scrape_number_of_results()

    def run(self):
        super().run()
        self.create_report_list()  # Assign New Data (Deeds & Mortgages)
        self.driver_utils.quit()
        self.busy = False

    # ---Handy Legend---
    # [0] = Direct Name
    # [1] = Indirect Name
    # [2] = Date and time (split by space to get either or)
    # [3] = Deed/mtg
    # [4] = "OR"
    # [5] = Book/Page
    # [6] = Legal desc
    # [7] = instrument #
    # [8] = consideration (with cents formatted .0000)
