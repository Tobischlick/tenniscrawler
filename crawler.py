import crawler
import helper
import time

Terminal = helper.Terminal()
Terminal.print("------------------------------start crawler-----------------------------")
t_start = time.perf_counter()

urlOne = "https://baden.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/leaguePage?championship=B1+S+2020"
urlTwo = "https://baden.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/leaguePage?championship=B2+S+2020"
urlThree = "https://baden.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/leaguePage?championship=B3+S+2020"
urlFour = "https://baden.liga.nu/cgi-bin/WebObjects/nuLigaTENDE.woa/wa/leaguePage?championship=B4+S+2020"

urls = [urlOne, urlTwo, urlThree, urlFour]
counter = 1

deleteDuplicate = helper.DeleteDuplicates()

files_leagues = []
for url in urls:
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
for file in files_clubsites:
    crawlMails = crawler.CrawledMails(file)
    crawlMails.fetch(counter)
    break

t_end = time.perf_counter()
d = t_end - t_start
if d >= 60:
    d = time.strftime("%M:%S", time.gmtime(d))
    d = f"{d}m"
else:
    d = f"{round(d, 2)}s"

Terminal.print(f"------------------------------end crawler: {d}------------------------------")