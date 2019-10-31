'''
Input: the copy-paste of the search criteria from the site
eg.
Fiscal Year From:	2018-2019
Fiscal Year To:	2018-2019
Area of Application:	Earth sciences
Engineering
Aquaculture
Commercial services
Sanitary engineering
Waste, waste management and recycling
By Institutions:	All

Output: a webdriver on the search results page 

Sub-function "go to page": 
input: a webdriver on the search results page, the page you want to go to
output: the webdriver on the page you want to go to


'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

INPUT_FILE = "inputdata/search_criteria.txt"
MULTIPLE_INPUTS = [
	"Area of Application",
]
SEARCH_URL = "http://www.nserc-crsng.gc.ca/ase-oro/index_eng.asp"

def parse_input_data(filename:str) -> dict:
	file = open(filename, 'r')
	lines = file.readlines()
	data = {}
	i = 0
	while (i < len(lines)):
		split = lines[i].split(":")
		key = split[0].strip()
		if key not in MULTIPLE_INPUTS:
			data[key] = split[1].strip()
		else:
			val = [split[1].strip()]
			for j in range(i+1, len(lines)):
				if ':' in lines[j]:
					i = j - 1
					break
				else:
					val.append(lines[j].strip())
			data[key] = val 
		i += 1 
	file.close()
	return data

def _create_new_webdriver():
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options)
	return driver 

def enter_data_on_website(search_criteria:dict):
	driver = _create_new_webdriver()
	driver.get(SEARCH_URL)
	fiscalyearfrom_select = Select(driver.find_element_by_id("fiscalyearfrom"))
	import pdb; pdb.set_trace();

	driver.quit()

def run():
	search_criteria = parse_input_data(INPUT_FILE)
	enter_data_on_website(search_criteria)

run()