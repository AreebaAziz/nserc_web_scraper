# NSERC Web Scraper for Engineering Outreach

This is a project done for the Engineering Outreach team. 

## Installation and Requirements

You need to have the following:

* Python 3.7
* git

To install, open a terminal and do the following steps:

1. Clone the repository:

``git clone https://github.com/AreebaAziz/nserc_web_scraper .`` 

2. Set up a Python virtual environment. 

Note: If your default ``python`` is 3.7, you don't need to add the 3.7 after ``python``.
Note 2: If you're on Windows, you will need to do ``. Scripts/activate`` instead of ``. bin/activate``.

```
python3.7 -m venv .
. bin/activate
```

3. Install Python dependencies:

``pip install -r requirements.txt``

## Tutorial

To run, do the following AFTER you've activated your virtual environment using ``. bin/activate``. 

``cd src && python run.py``

If everything is installed correctly, you should receive the following output:

```
(nserc_scraper) areeba@areebapc:~/school/engoutreach/nserc_scraper$ cd src && python run.py
[ error - not enough arguments. ]

usage: python run.py <WHAT_TO_RUN> [ARGS]

WHAT_TO_RUN can be:
    [1]  details_scraper <file/to/search-results-data.json> <file/to/output.csv>
```

To run the details_scraper, you need the input json file that contains data from the search results page, and a name of the csv output file you want to save the results to. 

On the NSERC awards search page, you can select filters for your search. Once you click the search button, you'll be directed to the results page containing a table of the awards that matched the filters. We want the data of all these awards. When you click on a specific award, you'll be directed to a details page for that award containing more data on the award. We want all this data. 

The details_scraper module does the second part of this process. Given input of a json file that contains the data on the search results page, it'll save the awards data onto a csv, as well as go through each award's details webpage and scrape the additional data for each award. 

The next step would be to automate the first part of the process. Currently, you have to manually enter the filters on the search page, click the search button, and then manually get the json data and save it to a file on your computer, and then run the script. It would be ideal if we got a webdriver to do the first half so that the only inputs would be the filters we want, and then the script could enter the filters on the search page and scrape all the data and save it into a csv. 

To get the json data of the awards table, do the following:

1. Go on the NSERC awards search page: https://www.nserc-crsng.gc.ca/ase-oro/index_eng.asp
2. Enter in your filters. Click the search button.
3. When you reach the search results page, go on the browser's developer tools. You can do this by clicking on the 3 bars thing on your browser's top right, then somewhere there should be Developer Tools or such. Click it, then go on the Network tab.
4. Refresh the page. You should now see a bunch of stuff appear on the network tool thing.
5. Find "ajax.asp?lang=e" item, it should be a POST request method. Click it. On the right side of the tool where it shows detail of that item, click on the "Response" tab. Find the plain text response that should be in JSON format. Copy all of it and save it on your computer in the same folder as src/ of this repo.
6. Now run the script again:

``python run.py details_scraper your_json_file.json your_output_file.csv``
7. If all goes well, the output will be saved in ``your_output_file.csv`` and you can view it on Excel or Google Sheets as a spreadsheet with all the awards' detailed data.

## Tools/Resources

I used several Python tools/libaries for this project. Here is a list of the most important ones. Feel free to google them to learn more about them.

* Python virtual environment 
* pip
* BeautifulSoup
* Python requests library 

To automate the part 1 of the process (entering filters, clicking search and getting the initial results table), you'll need a webdriver. 
* Selenium for Python
* you can use any web browser. geckodriver is the one you need for Firefox. chromedriver is what you need for Chrome. Read up the instructions online on how to install a webdrive for Selenium use. 
