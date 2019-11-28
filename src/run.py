'''
usage: python run.py <WHAT_TO_RUN> [ARGS]

WHAT_TO_RUN can be:
    [1]  details_scraper <file/to/search-results-data.json> <file/to/output.csv>
    [2]  scrape_all_awards <year_from> <year_to> <file/to/output.xlsx>
'''

import sys
import details_scraper as details_scraper_m
import scrape_all_awards

FUNCTION_MAP = {
	'1': 'details_scraper',
	'2': 'scrape_all_awards',
}

def scrape_all_awards():
	print("[ running scrape_all_awards ]")

	# validate arguments - we need 3 args for this function. 3 + 2 = 5 required args
	if (len(sys.argv) < 5):
		_usage_error("not enough arguments for this function.")

	try:
		year_from = int(sys.argv[2])
		year_to = int(sys.argv[3])
	except ValueError:
		_usage_error("year_from and year_to must be an integer.")

	output_file = sys.argv[4]

	scrape_all_awards.run(year_from, year_to)


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