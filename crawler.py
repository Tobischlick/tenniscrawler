import configparser
import time
from pathlib import Path
from src import helper, crawler

TERMINAL = helper.Terminal()
TERMINAL.print("------------------------------start crawler-----------------------------")
t_start = time.perf_counter()

config = configparser.ConfigParser()
config.read('.config/config.ini')
urls = dict(config['URLS'])

counter = 1

DELETE_DUPLICATE = helper.DeleteDuplicates()

files_leagues = []
for url in urls.values():
    print("url: " + url)
    crawl_groups = crawler.CrawledGroups(url)
    files_leagues.append(crawl_groups.fetch(counter))
    counter = counter + 1

counter = 1
files_clubs = []
for file in files_leagues:
    crawl_teams = crawler.CrawledTeams(file)
    files_clubs.append(crawl_teams.fetch(counter))
    counter = counter + 1

counter = 1
files_clubsites = []
for file in files_clubs:
    crawl_clubs = crawler.CrawledClubs(file)
    files_clubsites.append(crawl_clubs.fetch(counter))
    counter = counter + 1

for file in files_clubsites:
    DELETE_DUPLICATE.delete(file)

counter = 1
FILENAME_MAILS = "./Excelfiles/04_Mails.csv"
CHECK_FILE = Path(FILENAME_MAILS)

if CHECK_FILE.is_file():
    TERMINAL.print(f"File {FILENAME_MAILS} does already exist")
else:
    for file in files_clubsites:
        crawl_mails = crawler.CrawledMails(file)
        crawl_mails.fetch(counter, FILENAME_MAILS)
        counter = counter + 1

t_end = time.perf_counter()
d = t_end - t_start
if d >= 60:
    d = time.strftime("%M:%S", time.gmtime(d))
    d = f"{d}m"
else:
    d = f"{round(d, 2)}s"

TERMINAL.print(f"------------------------------end crawler: {d}------------------------------")
