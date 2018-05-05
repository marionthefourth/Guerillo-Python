# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:14:10 2018

@author: Panoramic, Co.
"""

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver as wd
import csv
import os
import bs4
from selenium.webdriver.common.keys import Keys
from datetime import date, time, datetime, timedelta
import time


class Pinellas:
    driver = None
    root_path = ""
    exports_path = ""
    reports_path = ""
    chrome_options = None
    status_label = None


    def __init__(self, status_label=None):
        self.status_label = status_label
        self.root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.exports_path = self.root_path + "\\bin\\exports\\"
        self.reports_path = self.root_path + "\\bin\\reports\\"
        chrome_options = wd.ChromeOptions()
        prefs = {'download.default_directory': self.exports_path}
        chrome_options.add_experimental_option('prefs', prefs)
        #chrome_options.add_argument("window-position=-10000,0")
        self.driver = wd.Chrome(self.root_path + "\\bin\\webdriver\\chromedriver.exe", chrome_options=chrome_options)
        #self.driver.set_window_position(-10000,0) #hides window without going headless (headless throws
                                                    # elementnotvisible exceptions and stuff)

    def wait_for_class(self, class_name, timeout=None, exit_message=""):
        if timeout is not None:
            start_time = time.time()
        while True:
            try:
                self.driver.find_element_by_class_name(class_name)
                break
            except NoSuchElementException:
                if timeout is not None:
                    if (time.time() - start_time) >= timeout:
                        print(exit_message)
                        self.driver.quit()
                        quit()
                pass

    def wait_for_id(self, id):  # TODO: need to add timeout functionality
        while (True):
            try:
                self.driver.find_element_by_id(id)
                break
            except NoSuchElementException:
                pass

    def wait_for_name(self, name):  # TODO: need to add timeout functionality
        while (True):
            try:
                self.driver.find_element_by_name(name)
                break
            except NoSuchElementException:
                pass

    def clear_and_send(self, ele_id, text_to_send):
        self.driver.find_element_by_id(ele_id).clear()
        self.driver.find_element_by_id(ele_id).send_keys(text_to_send)

    def csv_to_deeds_and_mortgages(self, file_name):
        # open file and turn the lines into a list of strings
        data_set = []
        with open(file_name, 'r') as file:
            data_set = file.readlines()
        # now convert the list of strings into a list of cleaned-up lists
        data_lists = []
        for item in data_set:
            data_lists.append(item.replace('"', "").replace("\n", "").split(","))
        # create two separate lists, one with deeds, the other with mortgages
        deeds = []
        mortgages = []
        for item in data_lists:
            if item[0] != "" and item[1] != "" and item[6] != "":
                if item[3] == "DEED": deeds.append(item)
                if item[3] == "MORTGAGE": mortgages.append(item)
        return (deeds, mortgages)

    def scrape_location_addresses_with_bookpage(self, bookpage_list, status_label=None):
        for (i, bookpage) in enumerate(bookpage_list):
            if i != 0:
                status_label.configure(text="Handling item " + str(i + 1 - 1) + " of " + str(len(bookpage_list) - 1))
                self.driver.get("http://www.pcpao.org/clik.html?pg=http://www.pcpao.org/searchbyOR.php")
                # have to accept, simulate with space press
                self.driver.find_element_by_tag_name("button").send_keys(Keys.SPACE)
                # wait to load
                self.wait_for_id("Text1")
                # get t'searchin
                self.driver.find_element_by_id("Text1").send_keys(bookpage[1])
                self.driver.find_element_by_name("submitButtonName").send_keys(Keys.SPACE)
                # wait for load, then get the link (hardcoded because always one result)
                self.wait_for_id("linkBar")

                aTags = self.driver.find_element_by_id("ITB").find_elements_by_tag_name("a")
                if len(aTags) == 0:
                    bookpage[1] = "No Book/Page"
                else:
                    self.driver.get(aTags[1].get_attribute("href").replace("general", "taxEst"))
                    # while True:
                    #     try:
                    #         self.driver.switch_to.default_content()
                    #         # wait for load, then switch to the frame with the data
                    #         self.wait_for_name("bodyFrame")
                    #         self.driver.switch_to.frame(self.driver.find_element_by_name("bodyFrame"))
                    #         # relaible way to get address is to go to tax estimator link from here
                    #         a_tags = []
                    #         a_tags = self.driver.find_elements_by_tag_name("a")
                    #         for tag in a_tags:
                    #             if tag.text == "Tax Estimator":
                    #                 self.driver.get(tag.get_attribute("href"))
                    #                 break
                    #         break
                    #     except UnexpectedAlertPresentException:
                    #         alert = self.driver.switch_to.alert
                    #         alert.accept()
                    # here we handle if we ended up at the tax assessor
                    button_tags = self.driver.find_elements_by_tag_name("button")
                    for button in button_tags:
                        if button.text == "I Agree":
                            button.send_keys(Keys.SPACE)
                    self.wait_for_id("addr_ns")
                    site_address = self.driver.find_element_by_id("addr_ns").get_attribute("value")
                    bookpage[1] = site_address
                    bookpage[6] = ""
                    bookpage[7] = ""

    def create_bookpage_list(self, deeds_list, mortgages_list):
        # remember that we're checking the mortgages (because we want those leads; deeds alone might not be the right kind)
        # but we need to pull the DEED bookpage number
        list = [["Name", "Address", "Date/Time", "Amount of Mortgage", "Property Sale Price"]]
        for entry in mortgages_list:
                for item in deeds_list:
                    if entry[0] == item[1]:  # checks the mortgage entry name to find the right deed item
                        list.append([entry[0], item[5], entry[2], entry[8], item[8], "", entry[6], item[0]])
                        # name from M, bookpage from D, date/time from M, mortgage amount from M, saleprice from D
                        # empty placeholder, legal descr, counterparty name

        return list

    def write_csv_file(self, file_name, list_of_lists, *args, **kwargs):
        mycsv = csv.writer(open(file_name, 'w', newline=''), *args, **kwargs)
        for row in list_of_lists:
            mycsv.writerow(row)

    def generate_nonbookpage_search_list(self,
                                         post_bookpage_list):  # sanitize name with comma formatting, legal description as components
        search_list = []
        i = 0
        for entry in post_bookpage_list:
            if entry[1] == "No Book/Page":
                # name is already LAST FIRST but just needs to be LAST, FIRST with comma
                # legal descr we want broken into a list of each word, space delimited from input
                sanitized_name = entry[7].split(" ")[0] + ", " + entry[7].split(" ")[1]
                search_list.append([sanitized_name, entry[6].split(" "), i])
            i = i + 1
        # so we're left with a list of lists, which are [0] - string, [1] - list
        return search_list

    def scrape_without_bookpage(self, search_list, main_list,
                                status_label=None):  # main list is the big original one where we add the site address
        i = 0
        for item in search_list:
            status_label.configure(text="Taking a deeper look for item " + str(i + 1) + " of " + str(len(search_list)))
            NAME_STRING = item[0]  # we'll be doing a query with the LAST, FIRST format name
            self.driver.get("http://www.pcpao.org/query_name.php?Text1=" + NAME_STRING + "&nR=1000")
            header = self.driver.find_element_by_tag_name("th")
            search_result_count = int(header.text.split("through ")[1].split(" of")[0])
            if search_result_count >= 50:
                print("Too many search results. Skipping this entry.")
                main_list[item[2]][1] = ""
            else:
                ITB = self.driver.find_element_by_id("ITB")  # main table with data
                ITB_td_tags = ITB.find_elements_by_tag_name("td")
                continue_search = True
                for tag in ITB_td_tags:  # if no results, remove the comma from name and search again
                    # this necessary b/c LLCs/entities
                    if tag.text == "Your search returned no records":
                        self.driver.get(
                            "http://www.pcpao.org/query_name.php?Text1=" + NAME_STRING.replace(",", "") + "&nR=1000")
                        ITB2 = self.driver.find_element_by_id("ITB")
                        ITB2_td_tags = ITB2.find_elements_by_tag_name("td")
                        for tag in ITB2_td_tags:
                            if tag.text == "Your search returned no records":  # if still no results, we're done
                                main_list[item[2]][1] = ""
                                main_list[item[2]][7] = ""
                                print("No results found for name " + item[0] + " with given legal description")
                                continue_search = False
                                break
                        break
                # now check for no results once more. if NOT no results, continue
                ITB = self.driver.find_element_by_id("ITB")  # main table with data
                if continue_search:
                    soup = bs4.BeautifulSoup(ITB.get_attribute("outerHTML"), "html.parser")
                    rows = soup.find_all('tr')
                    # now, row[*].find_all('td') returns a list that has each item comma delimited
                    # the 5 index should be the subdivision (which our legal description can look against)
                    # the 1 index is the a tag we can get the link from for the parcel
                    sub_and_link = []  # let's just make a list of the results to parse through firs
                    for row in rows:
                        row_list = row.find_all('td')
                        if len(row_list) >= 6:
                            sub_and_link.append([row_list[5].text, row_list[1].a['href']])
                    # now use the list to traverse legal description vs subdivision name
                    for line in sub_and_link:
                        match_found = False
                        match_count = 0  # we'll be counting the number of word matches (order unimportant)
                        # 2 or more matches should signify a hit
                        subdivision_searchable = line[0].split(" ")  # line[0] is the subdivision name
                        for word in item[1]:  # this was our input list with the space delimited legal descr.
                            for other_word in subdivision_searchable:
                                if word == other_word:
                                    match_count = match_count + 1
                            if match_count >= 2:
                                break
                        if match_count >= 2:
                            match_found = True
                            self.driver.get("http://www.pcpao.org/" + line[1].replace("general",
                                                                                      "taxEst"))  # this takes us to parcel
                            # while True:
                            #     try:
                            #         self.driver.switch_to.default_content()
                            #         # wait for load, then switch to the frame with the data
                            #         self.wait_for_name("bodyFrame")
                            #         self.driver.switch_to.frame(self.driver.find_element_by_name("bodyFrame"))
                            #         # relaible way to get address is to go to tax estimator link from here
                            #         a_tags = []
                            #         a_tags = self.driver.find_elements_by_tag_name("a")
                            #         for tag in a_tags:
                            #             if tag.text == "Tax Estimator":
                            #                 self.driver.get(tag.get_attribute("href"))
                            #                 break
                            #         break
                            #     except UnexpectedAlertPresentException:
                            #         alert = self.driver.switch_to.alert
                            #         alert.accept()
                            # here we handle if we ended up at the tax assessor
                            button_tags = self.driver.find_elements_by_tag_name("button")
                            for button in button_tags:
                                if button.text == "I agree":
                                    button.send_keys(Keys.SPACE)
                            self.wait_for_id("addr_ns")
                            site_address = self.driver.find_element_by_id("addr_ns").get_attribute("value")
                            main_list[item[2]][1] = site_address
                            main_list[item[2]][6] = ""
                            main_list[item[2]][7] = ""
                            break
                    if match_found == False:
                        main_list[item[2]][1] = ""
                        print("No results found for name " + item[0] + " with given legal description")
            i = i + 1

    def clean_final_list(self, main_list):
        bad_eggs = []
        for i,entry in enumerate(main_list):
            if entry[1] == "":
                bad_eggs.append(i)
        for bad_egg in reversed(bad_eggs):
            main_list.pop(bad_egg)
        print("End of method")
        print(main_list)

    def run(self, input_list):
        self.status_label.configure(text="Search starting")
        lower_bound = input_list[0]
        upper_bound = input_list[1]
        startDate = input_list[2]
        endDate = input_list[3]

        # store target URL as variable - this will be dynamic from user input (hills or pinellas)

        tURL = 'https://officialrecords.mypinellasclerk.org/search/SearchTypeConsideration'
        self.driver.get(tURL)
        self.status_label.configure(text="Searching...")
        # hit the accept button to be able to do anything else
        self.driver.find_element_by_id("btnButton").click()
        # date range entry
        clear_and_send_list = [["RecordDateFrom", startDate],
                               ["RecordDateTo", endDate],
                               ["LowerBound", lower_bound],
                               ["UpperBound", upper_bound]]
        for row in clear_and_send_list:
            self.clear_and_send(row[0], row[1])
        # time to search
        self.driver.find_element_by_id("btnSearch").click()
        # for it to load fully
        self.wait_for_class("t-grid-content", timeout=20, exit_message="No results found. Try a different query.")

        while True:
            try:
                self.driver.find_element_by_class_name("t-no-data")
            except NoSuchElementException:
                break
        # now we can just download the csv file provided
        self.driver.find_element_by_id("btnCsvButton").click()

        """--Let's crack open the cold one with the bois"""
        # wait for download
        start_time = time.time()
        while not os.path.isfile(self.exports_path + "\\SearchResults.csv"):
            if (time.time() - start_time) >= 8:
                print(
                    "Error in downloading data. Please try again. If the problem persists, cry heck and let loose the doggos of war.")
                self.driver.quit()
                quit()
            pass
        # rename
        nowTime = str(datetime.now()).replace(":", "").replace(".", "-")
        new_file_name = self.exports_path + "\\" + startDate.replace("/", "") + "-" + endDate.replace("/",
                                                     "")+" " + lower_bound + " " + upper_bound + " " + nowTime + ".csv"
        os.rename(self.exports_path + "\\SearchResults.csv", new_file_name)

        # call the method and assign the sexy new returned data
        d_and_m = self.csv_to_deeds_and_mortgages(new_file_name)
        d_list = d_and_m[0]
        m_list = d_and_m[1]

        new_bookpage_list = self.create_bookpage_list(d_list, m_list)
        self.status_label.configure(text="Processing " + str(len(new_bookpage_list)) + " items")
        self.scrape_location_addresses_with_bookpage(new_bookpage_list, status_label=self.status_label)
        main_list = new_bookpage_list  # now that first scrape was done, give it a more fitting name

        # time to now scrape for the ones that didn't have a bookpage
        secondary_searchable_list = self.generate_nonbookpage_search_list(main_list)
        self.status_label.configure(text="Now processing " + str(len(secondary_searchable_list)) + " items")
        self.scrape_without_bookpage(secondary_searchable_list, main_list,
                                     self.status_label)  # 2ndary list our check/trigger list, but
        # main_list is the one that will have the address injected
        self.clean_final_list(main_list)
        print("Second check outside of method")
        print(main_list)
        self.status_label.configure(text="Almost done. Wrapping up.")

        now = datetime.now()
        report_suffix = now.strftime("%Y-%m-%d %H-%M.csv")
        report_file_name = self.reports_path + report_suffix
        self.write_csv_file(report_file_name, main_list)

        self.driver.quit()
        os.startfile(report_file_name)

        # ---Handy Legend---
        # [0] = Direct Name
        # [1] = Indrect Name
        # [2] = Date and time (split by space to get either or)
        # [3] = Deed/mtg
        # [4] = "OR"
        # [5] = Book/Page
        # [6] = Legal desc
        # [7] = instrument #
        # [8] = consideration (with cents formatted .0000)
