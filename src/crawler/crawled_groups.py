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
        already_written = set()
        if check_file.is_file():
            with open(filename, newline="", encoding="utf-8") as csvfile_read:
                reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                already_written = {' '.join(row) for row in reader}
            logger.info("File %s already has %s rows, resuming", filename, len(already_written))
        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|')
            for link in links:
                url_link = urljoin(self.url, link.attrs["href"])
                if url_link in already_written:
                    logger.info("%s already present in %s, skipping", url_link, filename)
                    continue
                writer.writerow([url_link])
                csvfile.flush()
                logger.info("%s added to %s", link.text, filename)
                already_written.add(url_link)
                c = c + 1
        logger.info("%s returned", filename)
        return filename
