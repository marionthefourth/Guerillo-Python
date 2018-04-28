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

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
exports_path = root_path+"\\bin\\exports\\"
reports_path = root_path+"\\bin\\reports\\"
from selenium import webdriver as wd

chrome_options = wd.ChromeOptions()
prefs = {'download.default_directory': exports_path}
chrome_options.add_experimental_option('prefs', prefs)
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys
from datetime import date, time, datetime, timedelta

"""Functions--"""

def wait_for_class(class_name):  # TODO: need to add timeout functionality
    while True:
        try:
            driver.find_element_by_class_name(class_name)
            break
        except NoSuchElementException:
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
    for (i,bookpage) in enumerate(bookpage_list):
        if i!=0:
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
            #here we handle if we ended up at the tax assessor
            button_tags = driver.find_elements_by_tag_name("button")
            for button in button_tags:
                if button.text == "I agree":
                    button.send_keys(Keys.SPACE)
            wait_for_id("addr_ns")
            site_address = driver.find_element_by_id("addr_ns").get_attribute("value")
            bookpage[1] = site_address

def create_bookpage_list(deeds_list,mortgages_list): #only necessary for qualifying entries, i.e., old enough (~30 days)
    #remember that we're checking the mortgages (because we want those leads; deeds alone might not be the right kind)
    #but we need to pull the DEED bookpage number
    cutoff_date = date.today() - timedelta(days=30)
    list = [["Name","Address","Date/Time","Amount of Mortgage","Property Sale Price"]]
    for entry in mortgages_list:
        date_sold = datetime.strptime(entry[2].split(" ")[0], "%m/%d/%Y").date()
        if date_sold <= cutoff_date:
            for item in deeds_list:
                if entry[0] == item[1]:#checks the mortgage entry name to find the right deed item
                    list.append([entry[0], item[5], entry[2], entry[8],item[8]])#name from m.entry, bookpage from d.item
    return list

def writeCsvFile(file_name, list_of_lists, *args, **kwargs):
    mycsv = csv.writer(open(file_name, 'w', newline=''), *args, **kwargs)
    for row in list_of_lists:
        mycsv.writerow(row)

"""--Functions"""

startDate = "03/18/2018"
endDate = "03/19/2018"
lower_bound = "200000"
upper_bound = "500000"

# store target URL as variable - this will be dynamic from user input (hills or pinellas)
tURL = 'https://officialrecords.mypinellasclerk.org/search/SearchTypeConsideration'
driver = wd.Chrome(chrome_options=chrome_options)
driver.get(tURL)

# hit the accept button to be able to do anything else
driver.find_element_by_id("btnButton").click()
# date range entry
dateFrom = driver.find_element_by_id("RecordDateFrom")
dateFrom.clear()
dateFrom.send_keys(startDate)
dateTo = driver.find_element_by_id("RecordDateTo")
dateTo.clear()
dateTo.send_keys(endDate)
# upper/lower bound entry
lowerBound = driver.find_element_by_id("LowerBound")
lowerBound.clear()
lowerBound.send_keys(lower_bound)
upperBound = driver.find_element_by_id("UpperBound")
upperBound.clear()
upperBound.send_keys(upper_bound)
# time to search
driver.find_element_by_id("btnSearch").click()

# for it to load fully
wait_for_class("t-grid-content")
while True:
    try:
        driver.find_element_by_class_name("t-no-data")
    except NoSuchElementException:
        break
# now we can just download the csv file provided
driver.find_element_by_id("btnCsvButton").click()

"""--Let's crack open the cold one with the bois"""
# wait for download
while (not os.path.isfile(exports_path + "\\SearchResults.csv")):
    pass
# rename
nowTime = str(datetime.now()).replace(":", "").replace(".", "-")
new_file_name = exports_path + "\\" + startDate.replace("/", "") + "-" + endDate.replace("/", "") + " " + nowTime + ".csv"
os.rename(exports_path + "\\SearchResults.csv", new_file_name)

# call the method and assign the sexy new returned data
d_and_m = csv_to_deeds_and_mortgages(new_file_name)
d_list = d_and_m[0]
m_list = d_and_m[1]

new_bookpage_list = create_bookpage_list(d_list,m_list)
scrape_location_addresses_with_bookpage(new_bookpage_list)
print(new_bookpage_list)
now = datetime.now()
report_suffix = now.strftime("%Y-%m-%d %H-%M.csv")
report_file_name = reports_path+report_suffix

writeCsvFile(report_file_name,new_bookpage_list)

driver.close()
""" 
---Handy Legend---
[0] = Direct Name
[1] = Indrect Name
[2] = Date and time (split by space to get either or)
[3] = Deed/mtg
[4] = "OR"
[5] = Book/Page
[6] = Legal desc
[7] = instrument #
[8] = considerationg (with cents formated .0000)

"""


#TODO: Entirely reconfigure the logic for 'old enough'. Look through entire list of original data
#and grab book page. Do the bookpage search on all items older than a week
#any of the ones that don't return a result on the bookpage search are noted/logged
#those noted/logged then are searched for the convoluted way