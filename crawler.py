import crawler
import helper
import configparser
import time
from pathlib import Path

Terminal = helper.Terminal()
Terminal.print("------------------------------start crawler-----------------------------")
t_start = time.perf_counter()

config = configparser.ConfigParser()
config.read('.config/config.ini')
urls =  dict(config['URLS'])

counter = 1

deleteDuplicate = helper.DeleteDuplicates()

files_leagues = []
for url in urls.values():
    print("url: " + url)
    crawlGroups = crawler.CrawledGroups(url)
    files_leagues.append(crawlGroups.fetch(counter))
    counter = counter + 1

counter = 1
files_clubs = []
for file in files_leagues:
    crawlTeams = crawler.CrawledTeams(file)
    files_clubs.append(crawlTeams.fetch(counter))
    counter = counter + 1

counter = 1
files_clubsites = []
for file in files_clubs:
    crawlClubs = crawler.CrawledClubs(file)
    files_clubsites.append(crawlClubs.fetch(counter))
    counter = counter + 1

for file in files_clubsites:
    deleteDuplicate.delete(file)

counter = 1
filename_mails = "./Excelfiles/04_Mails.csv"
checkFile = Path(filename_mails)

if checkFile.is_file():
    Terminal.print(f"File {filename_mails} does already exist")
else:
    for file in files_clubsites:
        crawlMails = crawler.CrawledMails(file)
        crawlMails.fetch(counter, filename_mails)
        counter = counter + 1

t_end = time.perf_counter()
d = t_end - t_start
if d >= 60:
    d = time.strftime("%M:%S", time.gmtime(d))
    d = f"{d}m"
else:
    d = f"{round(d, 2)}s"

Terminal.print(f"------------------------------end crawler: {d}------------------------------")
