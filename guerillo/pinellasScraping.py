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
root_path = os.path.abspath(os.path.dirname(__file__))
from selenium import webdriver as wd
chrome_options = wd.ChromeOptions() 
prefs = {'download.default_directory' : root_path}
chrome_options.add_experimental_option('prefs', prefs)
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.keys import Keys
from datetime import date, time, datetime, timedelta


"""Functions--"""
def wait_for_class(class_name):#TODO: need to add timeout functionality
    while(True):
        try:
            driver.find_element_by_class_name(class_name)
            break
        except NoSuchElementException:
            pass
def wait_for_id(id):#TODO: need to add timeout functionality
    while(True):
        try:
            print("....")
            driver.find_element_by_id(id)
            break
        except NoSuchElementException:
            print(driver.page_source)
            pass
def wait_for_name(name):#TODO: need to add timeout functionality
    while(True):
        try:
            driver.find_element_by_name(name)
            break
        except NoSuchElementException:
            pass
"""--Functions"""

startDate = "03/18/2018"
endDate = "03/19/2018"
lower_bound = "200000"
upper_bound = "500000"

#store target URL as variable - this will be dynamic from user input (hills or pinellas)
tURL = 'https://officialrecords.mypinellasclerk.org/search/SearchTypeConsideration'
driver = wd.Chrome(chrome_options=chrome_options)
driver.get(tURL)

#hit the accept button to be able to do anything else
driver.find_element_by_id("btnButton").click()
#date range entry
dateFrom = driver.find_element_by_id("RecordDateFrom")
dateFrom.clear()
dateFrom.send_keys(startDate)
dateTo = driver.find_element_by_id("RecordDateTo")
dateTo.clear()
dateTo.send_keys(endDate)
#upper/lower bound entry
lowerBound = driver.find_element_by_id("LowerBound")
lowerBound.clear()
lowerBound.send_keys(lower_bound)
upperBound = driver.find_element_by_id("UpperBound")
upperBound.clear()
upperBound.send_keys(upper_bound)
#time to search
driver.find_element_by_id("btnSearch").click()

#for it to load fully
wait_for_class("t-grid-content")
while(True):
    try:
        driver.find_element_by_class_name("t-no-data")
    except NoSuchElementException:
        break
#now we can just download the csv file provided
driver.find_element_by_id("btnCsvButton").click()

"""--Let's crack open the cold one with the bois"""
#wait for download
while (not os.path.isfile(root_path+"\\SearchResults.csv")):
    pass
#rename
nowTime = str(datetime.now()).replace(":","").replace(".","-")
new_file_name = root_path+"\\"+startDate.replace("/","")+"-"+endDate.replace("/","")+" "+nowTime+".csv"
os.rename(root_path+"\\SearchResults.csv",new_file_name)


def csv_to_deeds_and_mortgages(file_name):
    #open file and turn the lines into a list of strings
    data_set = []
    with open(file_name,'r') as file:
        data_set = file.readlines()
    #now convert the list of strings into a list of cleaned-up lists
    data_lists = []
    for item in data_set:
        data_lists.append(item.replace('"',"").replace("\n","").split(","))
    #create two separate lists, one with deeds, the other with mortgages
    deeds = []
    mortgages = []
    for item in data_lists:
        if item[3]=="DEED": deeds.append(item)
        if item[3]=="MORTGAGE": mortgages.append(item)
    return (deeds,mortgages)

#call the method and assign the sexy new returned data
d_and_m = csv_to_deeds_and_mortgages(new_file_name)
d_list = d_and_m[0]
m_list = d_and_m[1]

#get setup for the book/page search check
cutoff_date = date.today()-timedelta(days=30)
#if it's old enough, add the direct name ([0]) and bookpage ([5]) to a list
bookpage_list=[]
for entry in m_list:
    date_sold = datetime.strptime(entry[2].split(" ")[0],"%m/%d/%Y").date()
    if date_sold <= cutoff_date:
        for item in d_list:
            if entry[0] == item[1]:
                bookpage_list.append([entry[0],item[5]])

#list is ready, lets pull up that pc POW!

#TODO: for loop for each bookpage_list item
for bookpage in bookpage_list:
    driver.get("http://www.pcpao.org/clik.html?pg=http://www.pcpao.org/searchbyOR.php")
    #have to accept, simulate with space press
    driver.find_element_by_tag_name("button").send_keys(Keys.SPACE)
    #wait to load
    wait_for_id("Text1")
    #get t'searchin
    driver.find_element_by_id("Text1").send_keys(bookpage[1])
    driver.find_element_by_name("submitButtonName").send_keys(Keys.SPACE)
    #wait for load, then get the link (hardcoded because always one result)
    wait_for_id("linkBar")
    aTags = driver.find_element_by_id("ITB").find_elements_by_tag_name("a")
    driver.get(aTags[1].get_attribute("href"))
    while(True):
        try:
            driver.switch_to_default_content()
            #wait for load, then switch to the frame with the data
            wait_for_name("bodyFrame")
            driver.switch_to_frame(driver.find_element_by_name("bodyFrame"))
            #relaible way to get address is to go to tax estimator link from here
            aTags = []
            aTags = driver.find_elements_by_tag_name("a")
            for tag in aTags:
                if tag.text == "Tax Estimator":
                    driver.get(tag.get_attribute("href"))
                    break
            break
        except UnexpectedAlertPresentException:
            alert = driver.switch_to.alert
            alert.accept()
    site_address = driver.find_element_by_id("addr_ns").get_attribute("value")
    bookpage[1]=site_address
   
#working now. just need to handle if it goes to 'i agree' page on tax collector
    

""" 
if date_sold <= cutoff_date: bookpage_list.append([entry[0],entry[5]])


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

time notes

cutoff_date = date.today()-timedelta(days=30)
for entry in mortgages:
    date_sold = datetime.strptime(entry[2].split(" ")[0],"%m/%d/%Y").date()
    print(date_sold <= cutoff_date)
    
for entry in mortgages:
    date_sold = datetime.strptime(entry[2].split(" ")[0],"%m/%d/%Y").date()
    if date_sold <= cutoff_date:
        print(entry[5])


"""


#data_table_html = driver.find_element_by_class_name("t-grid-content").get_attribute("outerHTML")
#
#
#data_soup = soup(data_table_html,"html.parser")
#data_rows = data_soup.find_all('tr')
#data = []
#for row in data_rows:
#    columns = row.find_all('td')
#    columns = [ele.text.strip() for ele in columns]
#    data.append([ele for ele in columns if ele]) # Get rid of empty values
#
#print(data)




