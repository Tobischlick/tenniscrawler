import csv
import logging
from urllib.parse import urljoin
from pathlib import Path
from bs4 import BeautifulSoup
from src.helper import http_client

logger = logging.getLogger(__name__)


class CrawledGroups:

    def __init__(self, url, session):
        self.url = url
        self.session = session
        logger.info("initialized CrawledGroups")

    def fetch(self, counter):
        c = 1
        r = http_client.get(self.session, self.url)
        doc = BeautifulSoup(r.text, "html.parser")
        table = doc.select_one(".result-set")
        links = table.find_all("a")
        filename = f"./Excelfiles/01_Gruppen_Bezirk_{counter}.csv"
        check_file = Path(filename)
        if check_file.is_file():
            logger.info("File %s does already exist", filename)
        else:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                logger.info("%s created", filename)
                writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                for link in links:
                    url_link = urljoin(self.url, link.attrs["href"])
                    writer.writerow([url_link])
                    logger.info("%s added to %s", link.text, filename)
                    c = c + 1
            logger.info("%s returned", filename)
        return filename
