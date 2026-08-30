import configparser
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from src import helper, crawler

Path("Logfiles").mkdir(exist_ok=True)
Path("Excelfiles").mkdir(exist_ok=True)

date = datetime.now().strftime("%d.%m.%y")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d.%m.%y - %H:%M:%S",
    handlers=[
        logging.FileHandler(f"Logfiles/{date}_log.txt", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

logger.info("------------------------------start crawler-----------------------------")
t_start = time.perf_counter()

config = configparser.ConfigParser()
config.read('.config/config.ini')
urls = dict(config['URLS'])

counter = 1

DELETE_DUPLICATE = helper.DeleteDuplicates()
session = helper.http_client.create_session()

files_leagues = []
for url in urls.values():
    logger.info("url: %s", url)
    crawl_groups = crawler.CrawledGroups(url, session)
    files_leagues.append(crawl_groups.fetch(counter))
    counter = counter + 1

counter = 1
files_clubs = []
for file in files_leagues:
    crawl_teams = crawler.CrawledTeams(file, session)
    files_clubs.append(crawl_teams.fetch(counter))
    counter = counter + 1

counter = 1
files_clubsites = []
for file in files_clubs:
    crawl_clubs = crawler.CrawledClubs(file, session)
    files_clubsites.append(crawl_clubs.fetch(counter))
    counter = counter + 1

for file in files_clubsites:
    DELETE_DUPLICATE.delete(file)

counter = 1
FILENAME_MAILS = "./Excelfiles/04_Mails.csv"

for file in files_clubsites:
    crawl_mails = crawler.CrawledMails(file, session)
    crawl_mails.fetch(counter, FILENAME_MAILS)
    counter = counter + 1

t_end = time.perf_counter()
d = t_end - t_start
if d >= 60:
    d = time.strftime("%M:%S", time.gmtime(d))
    d = f"{d}m"
else:
    d = f"{round(d, 2)}s"

logger.info("------------------------------end crawler: %s------------------------------", d)
