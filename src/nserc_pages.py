from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

writer = pd.ExcelWriter('/Users/kevin/Desktop/NSERCLinks.xlsx', engine='xlsxwriter')

# --------------------------------------------------------------
# ********* START UP CHROME AND GO TO THE NSERC WEBSITE ********
driver = webdriver.Chrome(executable_path=r'/Users/kevin/Desktop/chromedriver')
driver.get("https://www.nserc-crsng.gc.ca/ase-oro/Results-Resultats_eng.asp")


# ----------------------------------------
# ********* ENTER SEARCH CRITERIA ********
#fromFiscal = driver.find_element_by_id('fiscalyearfrom')

# Change CSS style to make it visible and select from and to fiscal year dropdown value
driver.execute_script("document.getElementById('fiscalyearfrom').style.display = 'block';")
Select(driver.find_element_by_css_selector('select#fiscalyearfrom')).select_by_value("1991")

time.sleep(5)

driver.execute_script("document.getElementById('fiscalyearto').style.display = 'block';")
Select(driver.find_element_by_css_selector('select#fiscalyearto')).select_by_value("2018")

# Change CSS style to make it visible and select area of application dropdown value
# ** NOTE: 703 = aerospace. You need to look up the values for each area.
#driver.execute_script("document.getElementById('AreaApplication').style.display = 'block';")
#Select(driver.find_element_by_css_selector('select#AreaApplication')).select_by_value("703")

# Launch your search criteria
driver.find_element_by_css_selector('#buttonSearch').click()


# -------------------------------------------------
# ********* NOW ON THE SEARCH RESULTS PAGE ********
time.sleep(15)

# Click on last button and go to last page
driver.find_element_by_css_selector('#result_last').click()
time.sleep(15)

# Get the number of pages by finding the value of the last page
pages = driver.find_element_by_css_selector('.paginate_active').get_attribute('innerHTML')
pages = int(pages)
time.sleep(15)

# Click on first button and go back to the first page
driver.find_element_by_css_selector('#result_first').click()
time.sleep(15)

# Establish variables for the while loop
linkList=[]
onPage=1

# while the current page number is <= the total number of pages
while onPage <= pages:
    # Get all the href links on the webpage
    links = driver.find_elements_by_xpath("//a[@href]")

    # Loop through each href element and get the link
    for link in links:
        href = link.get_attribute('href')
        
        # If the link is a detail link then append it to our list
        if 'Details-Detailles_eng.asp?id=' in href:
            linkList.append(href)

    # Click on next page button, let it load, and then add to the counter
    driver.find_element_by_css_selector('#result_next').click()
    time.sleep(15)
    onPage+=1

time.sleep(15)

driver.quit()

nsercLinks = pd.DataFrame(
    {'Link': linkList}
)

nsercLinks.to_excel(writer,sheet_name='Award Summary Links',index=False)
writer.save()
