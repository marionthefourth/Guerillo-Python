# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:14:10 2018

@author: Panoramic, Co.
"""
import os
from datetime import datetime

import bs4
from selenium.webdriver.common.keys import Keys

from guerillo.classes.backend_objects.county import County
from guerillo.classes.backend_objects.homeowner import Homeowner
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


class Pinellas(Scraper):
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
        for item in data_lists:
            if item[0] != "" and item[1] != "" and item[6] != "":
                if item[3] == General.DEED:
                    deeds.append(item)
                elif item[3] == General.MORTGAGE:
                    mortgages.append(item)
        return deeds, mortgages

    def pull_address_by_bookpage(self):
        for (i, homeowner) in enumerate(self.search_result.homeowners):
            self.status_label.configure(
                text="Handling item " + str(i + 1) + " of " + str(len(self.search_result.homeowners)))

            self.search_by_bookpage(homeowner.bookpage)
            # Get the link (hardcoded because always one result)
            addresses = self.driver_utils.driver.find_element_by_id(General.PCPAO.ITB).find_elements_by_tag_name(HTML.A)
            if len(addresses) != 0:
                address = self.get_site_address(
                    addresses[1].get_attribute(HTML.HREF).replace("general", General.PCPAO.TAX_EST))
                homeowner.address = address

    def create_bookpage_list(self, deeds_list, mortgages_list):
        #  Check Mortgages for Leads
        #  Get Deed Bookpages
        homeowners = list()
        for mortgage in mortgages_list:
            if mortgage[0] != "":  # Check if Mortgage has a name
                for deed in deeds_list:
                    if mortgage[0] == deed[1]:  # Check Mortgage Entry Name to find Deed Item
                        homeowners.append(Homeowner(mortgage_item=mortgage, deed_item=deed))

        self.search_result.homeowners = homeowners

    def create_report_list(self, file_name):
        deeds_and_mortgages = self.create_deeds_and_mortgages_list(file_name)
        self.create_bookpage_list(deeds_and_mortgages[0], deeds_and_mortgages[1])
        self.status_label.configure(text="Processing " + str(len(self.search_result.homeowners)) + " items")
        self.pull_address_by_bookpage()
        # Scrape for non-bookpage data
        self.status_label.configure(text="Now processing " + str(len(self.search_result.homeowners)) + " items")
        self.scrape_without_bookpage()  # 2nd list our check/trigger list, but
        # report_list is the one that will have the address injected
        self.search_result.clean()
        print(self.search_result.to_list())

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
            for word in homeowner.legal_description.split(" "):  # Input List w/ space delimited legal description.
                for other_word in subdivision_searchable:
                    if word == other_word:
                        match_count += 1
                if match_count >= 2:
                    break
            if match_count >= 2:
                return True, line

        return False, None

    def scrape_without_bookpage(self):
        for (i, homeowner) in enumerate(self.search_result.homeowners):
            if not homeowner.address:
                self.status_label.configure(text="Taking a deeper look for item " + str(i + 1) + " of " + str(
                    len(self.search_result.homeowners)))
                if self.get_search_result_count_by_name(homeowner.counterparty_name) <= 50:
                    if self.should_continue_search(homeowner.counterparty_name):
                        match_with_line = self.find_subdivision_match(homeowner)
                        if match_with_line[0]:
                            url = URLs.PCPAO.HOME + match_with_line[1][1].replace("general", General.PCPAO.TAX_EST)
                            homeowner.address = self.get_site_address(url)

    def rename_downloaded_csv_file(self, file_name):
        export_path = FileStorage.get_full_path(Folders.EXPORTS)

        end_date = Sanitizer.date(self.search_query.end_date)
        start_date = Sanitizer.date(self.search_query.start_date)
        current_date_time = Sanitizer.date_time(str(datetime.now()))

        renamed_downloaded_file_name = export_path + start_date + "-" + end_date + " " + current_date_time + ".csv"

        FileStorage.rename(file_name, renamed_downloaded_file_name)
        return renamed_downloaded_file_name

    def run(self):
        # Should receive from UI
        self.status_label.configure(text="Search starting")
        # UI After Tapping Search Data Button
        # store target URL as variable - this will be dynamic from user input (hills or pinellas)

        self.accept_terms_and_conditions()  # Pinellas Starts Here
        self.status_label.configure(text="Searching...")
        self.fill_search_query_fields()  # Data Ranges Entry
        downloaded_file_name = self.download_csv_file()  # Download CSV file provided and rename it

        # Assign New Data (Deeds & Mortgages)
        self.create_report_list(downloaded_file_name)
        # Update Report Data

        self.status_label.configure(
            text="Successfully found " + str(len(self.search_result.homeowners)) + " results. Wrapping up.")
        report_file_name = FileStorage.get_full_path(Folders.REPORTS) + datetime.now().strftime("%Y-%m-%d %H-%M.csv")
        FileStorage.save_data_to_csv(report_file_name, self.search_result.to_list())

        self.driver_utils.quit()
        os.startfile(report_file_name)

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
