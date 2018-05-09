# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:14:10 2018

@author: Panoramic, Co.
"""
import os
from datetime import datetime
import bs4
from selenium.webdriver.common.keys import Keys
from guerillo.classes.backend_objects.homeowner import Homeowner
from guerillo.classes.scrapers.scraper import Scraper
from guerillo.config import URLs, General, HTML, Folders, KeyFiles
from guerillo.utils.sanitizer import Sanitizer
from guerillo.utils.driver_utils import Action
from guerillo.utils.file_storage import FileStorage


class Pinellas(Scraper):

    def __init__(self, search_query=None, exports_path=None, status_label=None):
        super().__init__(search_query, exports_path)
        self.status_label = status_label

    def create_deeds_and_mortgages_list(self, file_name):
        data_lists = list()
        for item in FileStorage.read(file_name, county_filter="Pinellas"):
            data_lists.append(item.replace('"', "").replace("\n", "").split(","))

        deeds = list()
        mortgages = list()
        for item in data_lists:
            if item[0] != "" and item[1] != "" and item[6] != "":
                if item[3] == General.DEED:
                    deeds.append(item)
                elif item[3] == General.MORTGAGE:
                    mortgages.append(item)
        return deeds, mortgages

    def search_by_bookpage(self, bookpage):
        self.driver_utils.action_multi({
            0: {Action.GET: URLs.PCPAO.SEARCH_BY_OR},
            1: {Action.SEND_KEYS_BY_TAG: {General.BUTTON: Keys.SPACE}},  # Accept Disclaimer
            2: {Action.WAIT_FOR_ID: {General.TEXT_1: 8}},
            3: {Action.SEND_KEYS_BY_ID: {General.TEXT_1: bookpage}},
            4: {Action.SEND_KEYS_BY_NAME: {General.PCPAO.BUTTON_SUBMIT: Keys.SPACE}},
            5: {Action.WAIT_FOR_ID: {General.LINK_BAR: 8}}
        })

    def pull_address_by_bookpage(self):
        for (i, homeowner) in enumerate(self.search_result.homeowners):
            self.status_label.configure(
                text="Handling item " + str(i + 1 - 1) + " of " + str(len(self.search_result.homeowners) - 1))

            self.search_by_bookpage(homeowner.bookpage)
            # Get the link (hardcoded because always one result)
            addresses = self.driver_utils.driver.find_element_by_id(General.PCPAO.ITB).find_elements_by_tag_name(HTML.A)
            if len(addresses) != 0:
                address = self.get_site_address(
                    addresses[1].get_attribute(HTML.HREF).replace("general", General.PCPAO.TAX_EST))
                homeowner.address = address

    def get_site_address(self, url):
        return self.driver_utils.action_multi({
            0: {Action.GET: url},
            1: {Action.COMPLEX: {  # Should be @ Tax Accessor
                Action.FIND_TAG_NAME: General.BUTTON,
                Action.MATCH_TEXT: General.I_AGREE,
                Action.SEND_KEYS: Keys.SPACE
            }},
            2: {Action.WAIT_FOR_ID: {General.PCPAO.ADDR_NS: 8}},
            3: {Action.RETURN: {Action.FIND_ID: General.PCPAO.ADDR_NS, Action.GET_ATTRIBUTE: General.VALUE}}
        })

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

    def get_search_result_count_by_name(self, name):
        header = self.driver_utils.action_multi({
            0: {Action.GET: URLs.PCPAO.TEXT_1 + name + HTML.NUM_RESULTS_1000},
            1: {Action.RETURN: {Action.FIND_TAG_NAME: HTML.TH}}
        })
        if not hasattr(header, 'text'):
            return 1000
        return int(header.text.split("through ")[1].split(" of")[0])

    def should_continue_search(self, name):
        return self.driver_utils.action_multi({
            0: {Action.COMPLEX: {
                Action.RETURN_PREP: {False: {Action.MATCH_TEXT: 2}},
                Action.REPEAT_PREP: {0: {Action.FIND_ID: Action.GET}, 1: {Action.FIND_ID: Action.MATCH_TEXT}},
                Action.FIND_ID: General.PCPAO.ITB,
                Action.FIND_TAG_NAME: HTML.TD,
                Action.MATCH_TEXT: General.PCPAO.NO_RECORDS,
                Action.GET: URLs.PCPAO.TEXT_1 + Sanitizer.general_name(name) + HTML.NUM_RESULTS_1000,
                Action.RETURN: {}
            }},
        })

    def find_subdivision_match(self, supplementary_list_item):
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
            match_found = False
            match_count = 0  # Count number of word matches (order unimportant)
            # 2 or more matches should signify a hit
            subdivision_searchable = line[0].split(" ")  # line[0] = subdivision name
            for word in supplementary_list_item[1]:  # Input List w/ space delimited legal description.
                for other_word in subdivision_searchable:
                    if word == other_word:
                        match_count = match_count + 1
                if match_count >= 2:
                    break
            if match_count >= 2:
                return True, line

        return False

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
                            return

    def accept_terms_and_conditions(self):
        self.driver_utils.action_multi({
            0: {Action.GET: URLs.MyPinellasClerk.SEARCH_TYPE_CONSIDERATION},
            1: {Action.CLICK: General.PCPAO.BUTTON}  # Hit Accept Button
        })

    def fill_search_query_fields(self):
        self.driver_utils.action_multi({
            0: {Action.CLEAR_THEN_SEND: {
                General.PCPAO.RECORD_FROM: self.search_query.start_date,
                General.PCPAO.RECORD_TO: self.search_query.end_date,
                General.PCPAO.LOWER_BOUND: self.search_query.lower_bound,
                General.PCPAO.UPPER_BOUND: self.search_query.upper_bound
            }}
        })

    def download_csv_file(self):
        self.driver_utils.action_multi({
            0: {Action.CLICK: General.PCPAO.BUTTON_SEARCH},
            1: {Action.WAIT_FOR_CLASS: {HTML.T_GRID_CONTENT: 20}},
            2: {Action.WAIT_FOR_CLASS_EXCEPTION: {HTML.T_NO_DATA: 20}},
            3: {Action.CLICK: General.PCPAO.BUTTON_CSV}
        })

        downloaded_file_name = FileStorage.get_full_path(Folders.EXPORTS) + KeyFiles.SEARCH_RESULTS
        FileStorage.handle_timeout(self.driver_utils.driver, downloaded_file_name)  # Wait For Download
        return self.rename_downloaded_csv_file(downloaded_file_name)

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

        self.status_label.configure(text="Almost done. Wrapping up.")
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
