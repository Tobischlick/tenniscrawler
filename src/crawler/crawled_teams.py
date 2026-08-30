import csv
import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.helper import concurrent_fetch
from src.helper.checkpoint import Checkpoint

logger = logging.getLogger(__name__)


class CrawledTeams:
    def __init__(self, filepath, session):
        self.filepath = filepath
        self.session = session
        logger.info("initialized 'CrawledTeams'")

    def fetch(self, counter):
        filename = f"./Excelfiles/02_Mannschaften_Bezirk_{counter}.csv"
        checkpoint = Checkpoint(f"{filename}.checkpoint")
        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|')
            with open(self.filepath, newline="", encoding="utf-8") as csvfile_read:
                logger.info("read file: %s", self.filepath)
                reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                pending = []
                for row in reader:
                    url_league = ' '.join(row)
                    if checkpoint.is_done(url_league):
                        logger.info("%s already processed, skipping", url_league)
                        continue
                    pending.append(url_league)
                pending = list(dict.fromkeys(pending))

            for url_league, r, error in concurrent_fetch.fetch_all(self.session, pending):
                if error is not None:
                    logger.warning("Request to %s failed: %s. Skipping...", url_league, error)
                    checkpoint.mark_done(url_league)
                    continue
                doc = BeautifulSoup(r.text, "html.parser")
                table = doc.select_one(".result-set")

                if table is None:
                    logger.warning("Could not find table at %s. Skipping...", url_league)
                    checkpoint.mark_done(url_league)
                    continue

                links = table.find_all("a")
                for link in links:
                    url_link = urljoin(url_league, link.attrs["href"])
                    writer.writerow([url_link])
                    csvfile.flush()
                    logger.info("%s added to %s", link.text, filename)
                checkpoint.mark_done(url_league)
        checkpoint.close()
        logger.info("%s returned", filename)
        return filename
