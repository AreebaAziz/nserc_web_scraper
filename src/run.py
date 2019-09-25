import json
import csv
import requests
from bs4 import BeautifulSoup

COLUMN_TITLES = [
	'Name',
	'Project Title',
	'Amount',
	'Fiscal Year',
	'Program',
	'award_id',
]
DETAILS_URL = "http://www.nserc-crsng.gc.ca/ase-oro/Details-Detailles_eng.asp?id={award_id}"

def write_to_csv(data:list, output_filename:str, column_headers: list):
	output_file = open(output_filename, 'w')
	csvwriter = csv.writer(output_file)
	csvwriter.writerow(column_headers)
	for row in data:
		csvwriter.writerow(row)
	output_file.close()

def parse_data_from_json(json_filename: str):
	data_file = open(json_filename, 'r')
	raw_data = data_file.read()
	data_file.close()

	parsed_data = json.loads(raw_data)

	return parsed_data['aaData']

def get_data_from_details_page(award_id: int):
	# scrape data from details page given the award_id of a single award
	data = {}
	r = requests.get(DETAILS_URL.format(award_id=award_id))
	if (r.status_code == 200):
		html = r.content.decode()
		soup = BeautifulSoup(html)
		rows = soup.findAll('tr')
		for row in rows:
			tds = row.findAll('td')
			data[str(tds[0].findAll('strong')[0].contents).strip().replace('[', '').replace(']', '').replace(':', '').replace("'", '')] = str(tds[1].contents[0]).strip()
			data[str(tds[2].findAll('strong')[0].contents).strip().replace('[', '').replace(']', '').replace(':', '').replace("'", '')] = str(tds[3].contents[0]).strip()
	else:
		print("error in getting the webpage for award {} - error {}".format(award_id, r.status_code))
	return data 

def get_data_from_details_page_forall(data:dict):
	# given data, a dict of {award_id->data}, update the data with the details scraped from the detail page
	for award_id, data in data.items():
		details = get_data_from_details_page(award_id=award_id)
		data.update(details)

def sort_data_by_id(data:list):
	sorted_data = {}
	for item in data:
		sorted_data[item["award_id"]] = item
	return sorted_data

def convert_data_items_to_dict(data:list):
	new_data = []
	for row in data:
		data_dict = {}
		for i in range(len(COLUMN_TITLES)):
			data_dict[COLUMN_TITLES[i]] = row[i]
		new_data.append(data_dict)
	return new_data

def format_data_as_list_of_list(data:dict):
	column_headers = [
		'award_id',
		'Award Details URL',
		'Project Title',
		'Amount',
		'Fiscal Year',
		'Program',
	]
	rows = []
	for award_id, info in data.items():
		row_dict = {}
		row_dict[column_headers.index('Award Details URL')] = DETAILS_URL.format(award_id=award_id)
		for key, value in info.items():
			if (key not in column_headers):
				column_headers.append(key)
			row_dict[str(column_headers.index(key))] = value 
		keys = [int(i) for i in row_dict.keys()]
		row = [None] * (max(keys) + 1)
		for index, value in row_dict.items():
			row[int(index)] = value 
		rows.append(row)

	return rows, column_headers

def run():
	data = parse_data_from_json('rawdata/19912014_aerospace_200000.json')
	data = convert_data_items_to_dict(data)
	data = sort_data_by_id(data)
	get_data_from_details_page_forall(data)
	data, column_headers = format_data_as_list_of_list(data)
	write_to_csv(data, 'outputdata/19912014_aerospace_200000.csv', column_headers)

run()

