import csv
import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.helper import concurrent_fetch
from src.helper.checkpoint import Checkpoint

logger = logging.getLogger(__name__)


class CrawledClubs:

    def __init__(self, filepath, session):
        self.filepath = filepath
        self.session = session
        logger.info("initialized 'CrawledClubs'")

    def fetch(self, counter):
        filename = f"./Excelfiles/03_Clubs_Bezirk_{counter}.csv"
        checkpoint = Checkpoint(f"{filename}.checkpoint")
        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|')
            with open(self.filepath, newline="", encoding="utf-8") as csvfile_read:
                logger.info("read file: %s", self.filepath)
                reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                pending = []
                for row in reader:
                    club_url = ' '.join(row)
                    if checkpoint.is_done(club_url):
                        logger.info("%s already processed, skipping", club_url)
                        continue
                    pending.append(club_url)
                pending = list(dict.fromkeys(pending))

            for club_url, r, error in concurrent_fetch.fetch_all(self.session, pending):
                if error is not None:
                    logger.warning("Request to %s failed: %s. Skipping...", club_url, error)
                    checkpoint.mark_done(club_url)
                    continue
                doc = BeautifulSoup(r.text, "html.parser")
                table = doc.select_one(".result-set")

                if table is None:
                    logger.warning("Could not find table at %s. Skipping...", club_url)
                    checkpoint.mark_done(club_url)
                    continue

                links = table.find_all("a")
                if not links:
                    logger.warning("No links found in result-set at %s. Skipping...", club_url)
                    checkpoint.mark_done(club_url)
                    continue

                club = links[0].text.strip()
                urlsite = urljoin(club_url, links[0].attrs["href"])
                writer.writerow([urlsite])
                csvfile.flush()
                logger.info("%s added to %s", club, filename)
                checkpoint.mark_done(club_url)
        checkpoint.close()
        logger.info("%s returned", filename)
        return filename
