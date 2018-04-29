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
import csv
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
exports_path = root_path + "\\bin\\exports\\"
reports_path = root_path + "\\bin\\reports\\"
from selenium import webdriver as wd

chrome_options = wd.ChromeOptions()
prefs = {'download.default_directory': exports_path}
chrome_options.add_experimental_option('prefs', prefs)
import bs4
from selenium.webdriver.common.keys import Keys
from datetime import date, time, datetime, timedelta
import time

"""Functions--"""


def wait_for_class(class_name, timeout=None, exit_message=""):
    if timeout is not None:
        start_time = time.time()
    while True:
        try:
            driver.find_element_by_class_name(class_name)
            break
        except NoSuchElementException:
            if timeout is not None:
                if (time.time() - start_time) >= timeout:
                    print(exit_message)
                    driver.quit()
                    quit()
            pass


def wait_for_id(id):  # TODO: need to add timeout functionality
    while (True):
        try:
            driver.find_element_by_id(id)
            break
        except NoSuchElementException:
            pass


def wait_for_name(name):  # TODO: need to add timeout functionality
    while (True):
        try:
            driver.find_element_by_name(name)
            break
        except NoSuchElementException:
            pass


def clear_and_send(ele_id, text_to_send):
    driver.find_element_by_id(ele_id).clear()
    driver.find_element_by_id(ele_id).send_keys(text_to_send)


def csv_to_deeds_and_mortgages(file_name):
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
        if item[3] == "DEED": deeds.append(item)
        if item[3] == "MORTGAGE": mortgages.append(item)
    return (deeds, mortgages)


def scrape_location_addresses_with_bookpage(bookpage_list):
    for (i, bookpage) in enumerate(bookpage_list):
        if i != 0:
            driver.get("http://www.pcpao.org/clik.html?pg=http://www.pcpao.org/searchbyOR.php")
            # have to accept, simulate with space press
            driver.find_element_by_tag_name("button").send_keys(Keys.SPACE)
            # wait to load
            wait_for_id("Text1")
            # get t'searchin
            driver.find_element_by_id("Text1").send_keys(bookpage[1])
            driver.find_element_by_name("submitButtonName").send_keys(Keys.SPACE)
            # wait for load, then get the link (hardcoded because always one result)
            wait_for_id("linkBar")
            aTags = driver.find_element_by_id("ITB").find_elements_by_tag_name("a")
            if len(aTags) == 0:
                bookpage[1] = "No Book/Page"
            else:
                driver.get(aTags[1].get_attribute("href"))
                while True:
                    try:
                        driver.switch_to.default_content()
                        # wait for load, then switch to the frame with the data
                        wait_for_name("bodyFrame")
                        driver.switch_to.frame(driver.find_element_by_name("bodyFrame"))
                        # relaible way to get address is to go to tax estimator link from here
                        a_tags = []
                        a_tags = driver.find_elements_by_tag_name("a")
                        for tag in a_tags:
                            if tag.text == "Tax Estimator":
                                driver.get(tag.get_attribute("href"))
                                break
                        break
                    except UnexpectedAlertPresentException:
                        alert = driver.switch_to.alert
                        alert.accept()
                # here we handle if we ended up at the tax assessor
                button_tags = driver.find_elements_by_tag_name("button")
                for button in button_tags:
                    if button.text == "I agree":
                        button.send_keys(Keys.SPACE)
                wait_for_id("addr_ns")
                site_address = driver.find_element_by_id("addr_ns").get_attribute("value")
                bookpage[1] = site_address
                bookpage[6] = ""
                bookpage[7] = ""
                if bookpage[0] != "" and bookpage[1] != "":
                    bookpage[5] = "Very High"


def create_bookpage_list(deeds_list, mortgages_list):
    # remember that we're checking the mortgages (because we want those leads; deeds alone might not be the right kind)
    # but we need to pull the DEED bookpage number
    list = [["Name", "Address", "Date/Time", "Amount of Mortgage", "Property Sale Price", "Confidence"]]
    for entry in mortgages_list:
        if entry[0] != "":
            for item in deeds_list:
                if entry[0] == item[1]:  # checks the mortgage entry name to find the right deed item
                    list.append([entry[0], item[5], entry[2], entry[8], item[8], "", entry[6], item[0]])
                    # name from M, bookpage from D, date/time from M, mortgage amount from M, saleprice from D
                    # placeholder for confidence level, legal descr, counterparty name
    return list


def write_csv_file(file_name, list_of_lists, *args, **kwargs):
    mycsv = csv.writer(open(file_name, 'w', newline=''), *args, **kwargs)
    for row in list_of_lists:
        mycsv.writerow(row)


def test_run():  # TODO: actually compare legal desc to sub name
    # will likely need to pass in the info to this method
    NAME_STRING = "Test, Ernest"
    driver.get("http://www.pcpao.org/query_name.php?Text1=" + NAME_STRING + "&nR=1000")
    # remember an individual name is LAST, FIRST
    ITB = driver.find_element_by_id("ITB")
    soup = bs4.BeautifulSoup(ITB.get_attribute("outerHTML"), "html.parser")
    rows = soup.find_all('tr')
    # row[*].find_all('td') returns a list that has each item comma delimited
    # the 0 index should be the name which we need to check first
    # the 5 index should be the subdivision (which our legal description can look against)
    # the 1 index is the a tag we can get the link from for the parcel
    name_sub_link = []
    for row in rows:
        row_list = row.find_all('td')
        if len(row_list) >= 6:
            name_sub_link.append([row_list[0].text, row_list[5].text, row_list[1].a['href']])

    for row in name_sub_link:
        if row[0].lower() == NAME_STRING.lower():  # remember an individual name is LAST, FIRST
            # TODO: add logic for legal desc/sub checking here FIRST, then proceed to below
            driver.get("http://www.pcpao.org/" + row[2])


"""--Functions"""

startDate = "04/13/2018"
endDate = "04/21/2018"
lower_bound = "200000"
upper_bound = "600000"

# store target URL as variable - this will be dynamic from user input (hills or pinellas)
tURL = 'https://officialrecords.mypinellasclerk.org/search/SearchTypeConsideration'
driver = wd.Chrome(root_path + "\\bin\\webdriver\\chromedriver.exe", chrome_options=chrome_options)
driver.get(tURL)
# hit the accept button to be able to do anything else
driver.find_element_by_id("btnButton").click()
# date range entry
clear_and_send_list = [["RecordDateFrom", startDate],
                       ["RecordDateTo", endDate],
                       ["LowerBound", lower_bound],
                       ["UpperBound", upper_bound]]
for row in clear_and_send_list:
    clear_and_send(row[0], row[1])
# time to search
driver.find_element_by_id("btnSearch").click()
# for it to load fully
wait_for_class("t-grid-content", timeout=20, exit_message="No results found. Try a different query.")

while True:
    try:
        driver.find_element_by_class_name("t-no-data")
    except NoSuchElementException:
        break
# now we can just download the csv file provided
driver.find_element_by_id("btnCsvButton").click()

"""--Let's crack open the cold one with the bois"""
# wait for download
start_time = time.time()
while not os.path.isfile(exports_path + "\\SearchResults.csv"):
    if (time.time() - start_time) >= 8:
        print(
            "Error in downloading data. Please try again. If the problem persists, cry heck and let loose the doggos of war.")
        driver.quit()
        quit()
    pass
# rename
nowTime = str(datetime.now()).replace(":", "").replace(".", "-")
new_file_name = exports_path + "\\" + startDate.replace("/", "") + "-" + endDate.replace("/",
                                                                                         "") + " " + nowTime + ".csv"
os.rename(exports_path + "\\SearchResults.csv", new_file_name)

# call the method and assign the sexy new returned data
d_and_m = csv_to_deeds_and_mortgages(new_file_name)
d_list = d_and_m[0]
m_list = d_and_m[1]

new_bookpage_list = create_bookpage_list(d_list, m_list)
scrape_location_addresses_with_bookpage(new_bookpage_list)
secondary_searchable_list = new_bookpage_list
print(new_bookpage_list)
now = datetime.now()

# TODO: secondary search function run here on secondary_searchable_list

report_suffix = now.strftime("%Y-%m-%d %H-%M.csv")
report_file_name = reports_path + report_suffix
write_csv_file(report_file_name, new_bookpage_list)  # TODO: change the file to secondary_searchable_list

driver.close()
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
