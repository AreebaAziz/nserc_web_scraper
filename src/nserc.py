import pandas as pd
import requests
import re
import numpy as np
from selenium import webdriver

writer = pd.ExcelWriter('/Users/kevin/Desktop/NSERC_Output.xlsx', engine='xlsxwriter')
data = pd.read_excel('/Users/kevin/Desktop/NSERCLinks.xlsx',
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

def cleanTXT(string):
    text = string.replace('<td>','')
    text = text.replace('<h2>','')
    text = text.replace('\r\n','')
    text = text.encode('latin1').decode('utf8')
    text = text.strip()
    return text

for index,row in data.iterrows():
    html = requests.get(row["Link"])
    webpage = html.text

    indexstart = webpage.index('class="researchDetails"')
    indexend = webpage.index('</table>')
    details = webpage[indexstart:indexend]

    compy = details[details.index('Competition Year'):]
    compy = compy[compy.index('<td>'):]
    compy = compy[compy.index('<td>'):compy.index('</td>')]
    compy = cleanTXT(compy)
    compYears.append(compy)

    fiscal = details[details.index('Fiscal Year'):]
    fiscal = fiscal[fiscal.index('<td>'):]
    fiscal = fiscal[fiscal.index('<td>'):fiscal.index('</td>')]
    fiscal = cleanTXT(fiscal)
    fiscalYears.append(fiscal)

    lead = details[details.index('Project Lead Name'):]
    lead = lead[lead.index('<td>'):]
    lead = lead[lead.index('<td>'):lead.index('</td>')]
    lead = cleanTXT(lead)
    projLeads.append(lead)

    school = details[details.index('Institution'):]
    school = school[school.index('<td>'):]
    school = school[school.index('<td>'):school.index('</td>')]
    school = cleanTXT(school)
    schools.append(school)

    dept = details[details.index('Department'):]
    dept = dept[dept.index('<td>'):]
    dept = dept[dept.index('<td>'):dept.index('</td>')]
    dept = cleanTXT(dept)
    depts.append(dept)

    prov = details[details.index('Province'):]
    prov = prov[prov.index('<td>'):]
    prov = prov[prov.index('<td>'):prov.index('</td>')]
    prov = cleanTXT(prov)
    provs.append(prov)

    amount = details[details.index('Award Amount'):]
    amount = amount[amount.index('<td>'):]
    amount = amount[amount.index('<td>'):amount.index('</td>')]
    amount = cleanTXT(amount)
    amounts.append(amount)

    instal = details[details.index('Installment'):]
    instal = instal[instal.index('<td>'):]
    instal = instal[instal.index('<td>'):instal.index('</td>')]
    instal = cleanTXT(instal)
    instals.append(instal)

    prog = details[details.index('Program'):]
    prog = prog[prog.index('<td>'):]
    prog = prog[prog.index('<td>'):prog.index('</td>')]
    prog = cleanTXT(prog)
    programs.append(prog)

    comm = details[details.index('Selection Committee'):]
    comm = comm[comm.index('<td>'):]
    comm = comm[comm.index('<td>'):comm.index('</td>')]
    comm = cleanTXT(comm)
    committees.append(comm)

    sub = details[details.index('Research Subject'):]
    sub = sub[sub.index('<td>'):]
    sub = sub[sub.index('<td>'):sub.index('</td>')]
    sub = cleanTXT(sub)
    researchSubs.append(sub)

    area = details[details.index('Area of Application'):]
    area = area[area.index('<td>'):]
    area = area[area.index('<td>'):area.index('</td>')]
    area = cleanTXT(area)
    areaApps.append(area)

    partner = details[details.index('Partners'):]
    partner = partner[partner.index('<td>'):]
    partner = partner[partner.index('<td>'):partner.index('</td>')]
    partner = cleanTXT(partner)
    partners.append(partner.replace('<br />',','))

    co_research = details[details.index('Co-Researchers'):]
    co_research = co_research[co_research.index('<td>'):]
    co_research = co_research[co_research.index('<td>'):co_research.index('</td>')]
    co_research = cleanTXT(co_research)
    coResearchers.append(co_research.replace('<br />',','))

    awardID = row['Link'][row['Link'].index('id='):]
    awardID = awardID.replace('id=','')
    awardIDs.append(awardID)

    projTitle = webpage[webpage.index('main-container-1col'):]
    projTitle = projTitle[projTitle.index('<h2>'):projTitle.index('</h2>')]
    projTitle = cleanTXT(projTitle)
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
