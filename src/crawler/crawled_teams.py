import csv
import logging
from urllib.parse import urljoin
from pathlib import Path
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class CrawledTeams:
    def __init__(self, filepath):
        self.filepath = filepath
        logger.info("initialized 'CrawledTeams'")

    def fetch(self, counter):
        filename = f"./Excelfiles/02_Mannschaften_Bezirk_{counter}.csv"
        check_file = Path(filename)
        if check_file.is_file():
            logger.info("File %s does already exist", filename)
        else:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                logger.info("%s created", filename)
                with open(self.filepath, newline="", encoding="utf-8") as csvfile_read:
                    logger.info("read file: %s", self.filepath)
                    reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                    for row in reader:
                        url_league = ' '.join(row)
                        r = requests.get(url_league)
                        doc = BeautifulSoup(r.text, "html.parser")
                        table = doc.select_one(".result-set")

                        if table is None:
                            logger.warning("Could not find table at %s. Skipping...", url_league)
                            continue

                        links = table.find_all("a")
                        writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                        for link in links:
                            url_link = urljoin(url_league, link.attrs["href"])
                            writer.writerow([url_link])
                            logger.info("%s added to %s", link.text, filename)
            logger.info("%s returned", filename)
        return filename
