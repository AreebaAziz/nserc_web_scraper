'''
usage: python run.py <WHAT_TO_RUN> [ARGS]

WHAT_TO_RUN can be:
    [1]  details_scraper <file/to/search-results-data.json> <file/to/output.csv>
    [2]  scrape_all_awards <year_from> <year_to> 
    [3]  scrape_awards_4yrs <year1> <year2> <year3> <year4>
    [4]  scrape_details_from_links <file/to/nserc_links.xlsx>
'''

import sys
import details_scraper as details_scraper_m
import scrape_all_awards as scrape_all_awards_m

FUNCTION_MAP = {
	'1': 'details_scraper',
	'2': 'scrape_all_awards',
	'3': 'scrape_awards_4yrs',
	'4': 'scrape_details_from_links',
}

def scrape_details_from_links():
	print("[ running scrape_details_from_links ]")

	# validate arguments - we need 1 args for this function. 1 + 2 = 3 required args
	if (len(sys.argv) < 3):
		_usage_error("not enough arguments for this function.")

	input_file = sys.argv[2]

	scrape_all_awards_m.get_details_data(input_file)

def scrape_awards_4yrs():
	print("[ running scrape_awards_4yrs ]")

	# validate arguments - we need 4 args for this function. 4 + 2 = 6 required args
	if (len(sys.argv) < 6):
		_usage_error("not enough arguments for this function.")

	try:
		year1 = int(sys.argv[2])
		year2 = int(sys.argv[3])
		year3 = int(sys.argv[4])
		year4 = int(sys.argv[5])
	except ValueError:
		_usage_error("years must be integer values.")

	scrape_all_awards_m.run_concurrently([year1, year2, year3, year4])

def scrape_all_awards():
	print("[ running scrape_all_awards ]")

	# validate arguments - we need 2 args for this function. 2 + 2 = 4 required args
	if (len(sys.argv) < 4):
		_usage_error("not enough arguments for this function.")

	try:
		year_from = int(sys.argv[2])
		year_to = int(sys.argv[3])
	except ValueError:
		_usage_error("year_from and year_to must be an integer.")

	scrape_all_awards_m.run(year_from, year_to)

def details_scraper():
	print("[ running details_scraper ]")
	# validate arguments - we need 2 args for this function. Add that to the first 2 args = 4 required args
	if (len(sys.argv) < 4):
		_usage_error("not enough arguments for this function.")

	input_file = sys.argv[2]
	output_file = sys.argv[3]

	details_scraper_m.run(input_file, output_file)

def run():
	if (len(sys.argv) == 1):
		_usage_error("not enough arguments.")

	function_id = sys.argv[1]
	if function_id not in FUNCTION_MAP:
		_usage_error("%s is not a valid function id." % function_id)

	if FUNCTION_MAP[function_id] not in globals():
		print("[ error - %s function does not exist." % FUNCTION_MAP[function_id])
		sys.exit(1)

	globals()[FUNCTION_MAP[function_id]]()

def _usage_error(msg: str):
	print("[ error - %s ]" % msg)
	print(__doc__)
	sys.exit(1)

run()