# -*- coding: utf-8 -*-
"""
Created on Tue May  1 00:11:23 2018

@author: Kenneth
"""
from selenium import webdriver as wd
import os
"""
https://hillsborough.county-taxes.com/public/real_estate/parcels/A1653890000
165389-0000
so far all folio formats for tax est are the above^ reformatted
A1653890000
so "A"+folio_string.replace("-","")

"""
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
exports_path = root_path + "\\bin\\exports\\"
reports_path = root_path + "\\bin\\reports\\"
chrome_options = wd.ChromeOptions()
prefs = {'download.default_directory': exports_path}
chrome_options.add_experimental_option('prefs', prefs)
driver = wd.Chrome(root_path + "\\bin\\webdriver\\chromedriver.exe", chrome_options=chrome_options)



"""Property Appraiser Traverse & Scrape Logic"""
name_string = "SMITH JACK L"
name_to_search = name_string.split(" ")[0]+", "+name_string.split(" ")[1]
                 #this example should be "SMITH, JACK"
driver.get(
        "http://gis.hcpafl.org/propertysearch/#/search/basic/owner="
        +name_to_search
        +"&pagesize=80"
)
table = driver.find_element_by_id("table-basic-results")
table_tr_tags = table.find_elements_by_tag_name("tr")
cleaned_rows = []
for tr_tag in table_tr_tags:
    td_tags = tr_tag.find_elements_by_tag_name("td")
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

#this javascript you can just click the row WebElement as a whole:
###EXAMPLE:
table_tr_tags[2].click()
### after clicking, then this logic (dynamc, not just example anymore):
legal_description = ""
body_tags = driver.find_elements_by_tag_name("tbody")
for body_tag in body_tags:
    if body_tag.get_attribute("data-bind")=="foreach: fullLegal()":
        legal_description = body_tag.text
        

