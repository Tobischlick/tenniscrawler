import csv
import logging
from urllib.parse import urljoin
from pathlib import Path
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class CrawledClubs:

    def __init__(self, filepath):
        self.filepath = filepath
        logger.info("initialized 'CrawledClubs'")

    def fetch(self, counter):
        c = 1
        filename = f"./Excelfiles/03_Clubs_Bezirk_{counter}.csv"
        check_file = Path(filename)
        if check_file.is_file():
            logger.info("File %s does already exist", filename)
        else:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                logger.info("%s created", filename)
                with open(self.filepath, newline="", encoding="utf-8") as csvfile_read:
                    logger.info("read file: %s", self.filepath)
                    reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                    writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                    for row in reader:
                        club_url = ' '.join(row)
                        r = requests.get(club_url)
                        doc = BeautifulSoup(r.text, "html.parser")
                        table = doc.select_one(".result-set")

                        if table is None:
                            logger.warning("Could not find table at %s. Skipping...", club_url)
                            continue

                        links = table.find_all("a")
                        club = links[0].text.strip()
                        urlsite = urljoin(club_url, links[0].attrs["href"])
                        writer.writerow([urlsite])
                        logger.info("%s added to %s", club, filename)
                        c = c + 1
            logger.info("%s returned", filename)
        return filename
