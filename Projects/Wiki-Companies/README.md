# Wikipedia Company Firmographics
==============================

This is a web scraping projects fro extracting informations about all the companies in all across United States.

## Project Organization
------------
    ├── LICENSE
	│
    ├── Makefile             <- Makefile with various commands 
	│
    ├── README.md       <- The top-level README for developers using this project.
	│
    ├── config               <- The configuration script for Scrapy.
	│
    ├── scraped_data
    │   ├── csv              <- Data generated in csv format from the raw json file.
    │   ├── excel           <- For better data analysis, generated in excel format from the raw json file.
    │   └── Json            <- The original, immutable data dump.
	│  
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── scraped_data
    │   ├── csv            <- Data generated in csv format from the raw json file.
    │   ├── excel          <- For better data analysis, generated in excel format from the raw json file.
    │   └── Json           <- The original, immutable data dump.
    │
    ├── docs               <- A Powerpoint slide is uploaded to illustrate the scraping approach.
    │
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
	│
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── Wiki_Companies    <- Necessary Scripts for structruring files
	│        ├──  __init__.py
	│        ├── data_generator
	│        		├── dataframe.py  <- For data Inspection and generation of new extention from the original data.
	│        ├── settings.py			  <-  For tweaking various settings like 'user-agents' and 'proxies'
	│        ├── middlewares.py	  <- Additional customized support.
	│        ├── pipelines.py		  <- For database support.
    │        ├── spiders       		<- Spiders for crawling and scraping data from websites
	│            	├── link_collection.py   	<- spider script for crawling on the targeted links, scrape all type of links and store company links.
	│            	├── link_extraction.py   	<- spider script for extracting links classified as regional and append new links to a pre-existing links file.
	│            	├── data_scraping.py   	<- spider script that is solely utilized for scraping firmographics from each company link.
    │    
    │   
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------
