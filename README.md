# TennisCrawler

## How to config

Config is located [here](.config/config.ini)

There are two things that you can configure:

### URLS

- The name of the keys doesn't matter, just the values are used. Here you can list the links of 'Bezirk' (by default all
  of them in Baden)

### MAILS

- The Type of mail you want to crawl. Naming of the key's is not important

You might have to install some packages like 'request' or 'beautifulsoup4', just use pip install.

## How to start

- If not existing, create the directories 'Logfiles' and 'Excelfiles' on root level
- Install the necessary libs via pip install (if you use linux, i recommend to use a virtual environment, as described now)
  - python3 -m venv venv
  - source venv/bin/activate

Run the crawler with `python crawler.py`. The result is a .csv file named '04_Mails.csv' with the following columns:

- 'Position'
- 'E-Mail'
- 'Bezirk'

You can simply convert the .csv file to an Excel table.