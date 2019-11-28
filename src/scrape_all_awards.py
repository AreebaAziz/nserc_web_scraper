import pandas as pd
import requests
import re
import numpy as np
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

LINKS_OUTPUT_FILE = "tmp/NSERCLinks_{year_from}-{year_to}_{timestamp}.xlsx"
NSERC_URL = "https://www.nserc-crsng.gc.ca/ase-oro/Results-Resultats_eng.asp"

def _get_timestamp():
    t = datetime.now()
    return "" + str(t.year) + "-" + str(t.month) + "-" + str(t.day) + "_" + str(t.hour) + str(t.minute)

def get_nserc_links(year_from:int, year_to:int):

    timestamp = _get_timestamp()
    links_output_file = LINKS_OUTPUT_FILE.format(year_from=year_from, year_to=year_to, timestamp=timestamp)

    writer = pd.ExcelWriter(links_output_file, engine='xlsxwriter')

    # --------------------------------------------------------------
    # ********* START UP CHROME AND GO TO THE NSERC WEBSITE ********
    driver = webdriver.Chrome(executable_path=r'/Users/kevin/Desktop/chromedriver')
    driver.get(NSERC_URL)


    # ----------------------------------------
    # ********* ENTER SEARCH CRITERIA ********
    #fromFiscal = driver.find_element_by_id('fiscalyearfrom')

    # Change CSS style to make it visible and select from and to fiscal year dropdown value
    driver.execute_script("document.getElementById('fiscalyearfrom').style.display = 'block';")
    Select(driver.find_element_by_css_selector('select#fiscalyearfrom')).select_by_value(str(year_from))

    time.sleep(5)

    driver.execute_script("document.getElementById('fiscalyearto').style.display = 'block';")
    Select(driver.find_element_by_css_selector('select#fiscalyearto')).select_by_value(str(year_to))

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

    return links_output_file

def _cleanTXT(string):
    text = string.replace('<td>','')
    text = text.replace('<h2>','')
    text = text.replace('\r\n','')
    text = text.encode('latin1').decode('utf8')
    text = text.strip()
    return text

def get_details_data(nserc_links_outputfile:str):
    data_output_file = nserc_links_outputfile.replace("NSERCLinks_", "AwardsOutput_")
    writer = pd.ExcelWriter(data_output_file, engine='xlsxwriter')
    data = pd.read_excel(nserc_links_outputfile,
                         sheet_name="Award Summary Links",dtype=str)

    awardIDs=[]
    projTitles=[]
    amounts=[]
    programs=[]
    committees=[]
    coResearchers=[]
    compYears=[]
    fiscalYears=[]
    projLeads=[]
    schools=[]
    depts=[]
    provs=[]
    instals=[]
    researchSubs=[]
    areaApps=[]
    partners=[]


    for index,row in data.iterrows():
        html = requests.get(row["Link"])
        webpage = html.text

        indexstart = webpage.index('class="researchDetails"')
        indexend = webpage.index('</table>')
        details = webpage[indexstart:indexend]

        compy = details[details.index('Competition Year'):]
        compy = compy[compy.index('<td>'):]
        compy = compy[compy.index('<td>'):compy.index('</td>')]
        compy = _cleanTXT(compy)
        compYears.append(compy)

        fiscal = details[details.index('Fiscal Year'):]
        fiscal = fiscal[fiscal.index('<td>'):]
        fiscal = fiscal[fiscal.index('<td>'):fiscal.index('</td>')]
        fiscal = _cleanTXT(fiscal)
        fiscalYears.append(fiscal)

        lead = details[details.index('Project Lead Name'):]
        lead = lead[lead.index('<td>'):]
        lead = lead[lead.index('<td>'):lead.index('</td>')]
        lead = _cleanTXT(lead)
        projLeads.append(lead)

        school = details[details.index('Institution'):]
        school = school[school.index('<td>'):]
        school = school[school.index('<td>'):school.index('</td>')]
        school = _cleanTXT(school)
        schools.append(school)

        dept = details[details.index('Department'):]
        dept = dept[dept.index('<td>'):]
        dept = dept[dept.index('<td>'):dept.index('</td>')]
        dept = _cleanTXT(dept)
        depts.append(dept)

        prov = details[details.index('Province'):]
        prov = prov[prov.index('<td>'):]
        prov = prov[prov.index('<td>'):prov.index('</td>')]
        prov = _cleanTXT(prov)
        provs.append(prov)

        amount = details[details.index('Award Amount'):]
        amount = amount[amount.index('<td>'):]
        amount = amount[amount.index('<td>'):amount.index('</td>')]
        amount = _cleanTXT(amount)
        amounts.append(amount)

        instal = details[details.index('Installment'):]
        instal = instal[instal.index('<td>'):]
        instal = instal[instal.index('<td>'):instal.index('</td>')]
        instal = _cleanTXT(instal)
        instals.append(instal)

        prog = details[details.index('Program'):]
        prog = prog[prog.index('<td>'):]
        prog = prog[prog.index('<td>'):prog.index('</td>')]
        prog = _cleanTXT(prog)
        programs.append(prog)

        comm = details[details.index('Selection Committee'):]
        comm = comm[comm.index('<td>'):]
        comm = comm[comm.index('<td>'):comm.index('</td>')]
        comm = _cleanTXT(comm)
        committees.append(comm)

        sub = details[details.index('Research Subject'):]
        sub = sub[sub.index('<td>'):]
        sub = sub[sub.index('<td>'):sub.index('</td>')]
        sub = _cleanTXT(sub)
        researchSubs.append(sub)

        area = details[details.index('Area of Application'):]
        area = area[area.index('<td>'):]
        area = area[area.index('<td>'):area.index('</td>')]
        area = _cleanTXT(area)
        areaApps.append(area)

        partner = details[details.index('Partners'):]
        partner = partner[partner.index('<td>'):]
        partner = partner[partner.index('<td>'):partner.index('</td>')]
        partner = _cleanTXT(partner)
        partners.append(partner.replace('<br />',','))

        co_research = details[details.index('Co-Researchers'):]
        co_research = co_research[co_research.index('<td>'):]
        co_research = co_research[co_research.index('<td>'):co_research.index('</td>')]
        co_research = _cleanTXT(co_research)
        coResearchers.append(co_research.replace('<br />',','))

        awardID = row['Link'][row['Link'].index('id='):]
        awardID = awardID.replace('id=','')
        awardIDs.append(awardID)

        projTitle = webpage[webpage.index('main-container-1col'):]
        projTitle = projTitle[projTitle.index('<h2>'):projTitle.index('</h2>')]
        projTitle = _cleanTXT(projTitle)
        projTitles.append(projTitle)

    nserc = pd.DataFrame(
        {'Award ID': awardIDs,
         'Competition Year': compYears,
         'Fiscal Year': fiscalYears,
         'Program': programs,
         'Selection Committee': committees,
         'Amount': amounts,
         'Installment': instals,
         'Research Subject': researchSubs,
         'Area of Application': areaApps,
         'Project Title': projTitles,
         'Project Lead Name': projLeads,
         'Co-Researchers': coResearchers,
         'Institution': schools,
         'Department': depts,
         'Province': provs,
         'Partners': partners
        }
    )

    nserc.to_excel(writer,sheet_name='Award Summaries',index=False)
    writer.save()

    return data_output_file

def run(year_from:int, year_to:int): 
    print("[ getting the NSERC links ]")
    nserc_links_outputfile = get_nserc_links(year_from, year_to)
    print("[ getting NSERC links done, data saved to {} ]".format(nserc_links_outputfile))
    print("[ getting the details data for each award ]")
    data_output_file = get_details_data(nserc_links_outputfile)
    print("[ done getting details data, saved to {} ]".format(data_output_file))