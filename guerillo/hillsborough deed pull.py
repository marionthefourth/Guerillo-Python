# -*- coding: utf-8 -*-
"""
Created on Tue May  1 22:05:12 2018

@author: Kenneth
"""
from selenium import webdriver as wd
import os
from datetime import datetime

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
exports_path = root_path + "\\bin\\exports\\"
reports_path = root_path + "\\bin\\reports\\"
chrome_options = wd.ChromeOptions()
prefs = {'download.default_directory': exports_path}
chrome_options.add_experimental_option('prefs', prefs)
driver = wd.Chrome(root_path + "\\bin\\webdriver\\chromedriver.exe", chrome_options=chrome_options)


lower_bound = "200000"
upper_bound = "600000"
start_date = "04/01/2018"
end_date = "04/03/2018"
today_date = datetime.today().strftime("%m/%d/%Y")


url_string = "https://pubrec3.hillsclerk.com/oncore/search.aspx?bd="+ start_date + "&ed=" + end_date + "&bt=O&lb="+lower_bound +"&ub=" +upper_bound+"&pt=-1&dt=MTG&st=consideration"
driver.get(url_string)
#doing the straight to URL method saves a little bit of pain
#however we want to maximize the search results. we have to click a 'setings' link
#then handle the fact that it pops up in a new window.
#the below chunk handles clicking that link and focusing the popup
main_window_handle = None
while not main_window_handle:
    main_window_handle = driver.current_window_handle
driver.find_element_by_id("PageHeader1_hlSettings").click()
settings_window_handle = None
while not settings_window_handle:
    for handle in driver.window_handles:
        if handle != main_window_handle:
            settings_window_handle = handle
            break
driver.switch_to.window(settings_window_handle)
#now we just need to manipulate the results count and submit
driver.find_element_by_id("cboResultCount").send_keys("500")
driver.find_element_by_id("cmdSubmit").click()
#that window doesn't exist but our driver is still focused on it
#we need to focus back. we already saved main_handle as a variable
#so we can just use that
driver.switch_to.window(main_window_handle)
#now that we're back, we'll have to reload the search
#given potential speed issues, but the fact that we can't wait for id
#(beacuse the ids of what we want are already there, we just don't have
#all the results displayed in chunks of 500, but instead 30)
#so we'll do an all encompassing check:
stale_page = driver.page_source
driver.find_element_by_id("cmdSubmit").click()
while driver.page_source == stale_page:
    pass
#we should be good now, so on to table shenanigans
#TODO: check if using bs4 to parse is faster. PROBABLY IS THO

table = driver.find_element_by_id("dgResults")
table_rows = table.find_elements_by_tag_name("tr")
data_results = ["Mortgage Amount","Full Name","Counterparty Name","Date","Legal Description"]
for row in table_rows:
    rc = row.find_elements_by_tag_name("td") #rc = row_columns
    if len(rc)>=12:
        data_results.append([
                rc[3].text,rc[4].text,rc[5].text,rc[6].text,rc[11].text
        ])


print(data_results)
"""
Columns by Header
1: Result/Row#
2: Status (????)
3: Mortgage Amount
4: Full Name
5: Counterparty Name
6: Date
7: Document Type
8: Book (O = official record)
9: Book #
10: Page #
11: Legal Desc
9: Instrument #

Only really need 3,4,5,6,11
"""
#TODO: handle max limit of 2000 searchs (hills may need to be limited)
#TODO: maybe just search mortgages, then look for that deed through more queries
#TODO: 