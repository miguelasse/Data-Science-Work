# Tennis Scraper #

The tennis scraper program allows users to scrape the ITF junior rankings 
to find their UTR (Universal 
Tennis Ranking) websites using BeautifulSoup and Selenium. It then 
transforms 
the data using Pandas and exports two CSVs to the user consisting of:
  
* The ITF junior rankings page (consisting of US and international 
players) and their associated UTR ID / Ranking.

## Table of Contents ##

* [Setup](#setup)
* [Running The Program](#running)

### Setup ###

The scraper assumes the user has installed Python and the required packages in requirements.txt.

### Running The Program ###

To run the program:

1. Set up the config.yml file with the specified URLs and ids needed, along with credentials and the export path to save to.
1. Once that's done, simply run the program in the Python interpreter of choice by executing the codeblock below.
1. In order to scrape the ITF website correctly, the program will ask the user to input the cookies from their browser into the command line. To get cookies from Chrome, for example, the user will:
    * Go to the ITF rankings page.
    * Open Chrome Dev Tools (right-click and choose "Inspect")
    * The default is "Elements". Choose "Application" on the top tabbed bar.
    * On the left-hand side under "Storage"the user will see "Cookies" that they can click.
    * Take the first two string values, generally these are long strings that start with "incap_XYZ" and "j/ABC123".

```python
python tennis_scraper.py
```

A progress bar will show progress as the program runs.
