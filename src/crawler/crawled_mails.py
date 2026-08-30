import configparser
import csv
import logging
from pathlib import Path
from bs4 import BeautifulSoup
from src.helper import concurrent_fetch
from src.helper.checkpoint import Checkpoint

logger = logging.getLogger(__name__)


class CrawledMails:
    def __init__(self, filepath, session):
        self.filepath = filepath
        self.session = session
        logger.info("initialized CrawledMails")

    def fetch(self, counter, filename_mails):
        config = configparser.ConfigParser()
        config.read('.config/config.ini')
        mails_config = dict(config['MAILS'])

        checkpoint = Checkpoint(f"{self.filepath}.mails-checkpoint")
        mails_file = Path(filename_mails)
        write_header = not mails_file.is_file() or mails_file.stat().st_size == 0

        with open(filename_mails, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|')
            if write_header:
                writer.writerow(['Position', 'E-Mail', 'Bezirk'])
                csvfile.flush()
            with open(self.filepath, newline="", encoding="utf-8") as csvfile_read:
                logger.info("read file: %s", self.filepath)
                reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                pending = []
                for row in reader:
                    url_clubsite = ' '.join(row)
                    if checkpoint.is_done(url_clubsite):
                        logger.info("%s already processed, skipping", url_clubsite)
                        continue
                    pending.append(url_clubsite)
                pending = list(dict.fromkeys(pending))

            for url_clubsite, r, error in concurrent_fetch.fetch_all(self.session, pending):
                if error is not None:
                    logger.warning("Request to %s failed: %s. Skipping...", url_clubsite, error)
                    checkpoint.mark_done(url_clubsite)
                    continue
                doc = BeautifulSoup(r.text, "html.parser")
                finder = doc.find_all("td")
                for i in range(0, len(finder)):
                    mail_type = finder[i].text
                    for mail_pattern in mails_config.values():
                        if mail_type == mail_pattern:
                            if i + 3 >= len(finder):
                                logger.warning(
                                    "No mail cell found for '%s' at %s. Skipping...",
                                    mail_type, url_clubsite)
                                break
                            mail_string = finder[i + 3].string
                            if mail_string != "-" and mail_string != "":
                                mail = self.encode_mail(mail_string, url_clubsite)
                                if mail is not None:
                                    writer.writerow([mail_type, mail, counter])
                                    csvfile.flush()
                                    logger.info(
                                        "Mail '%s' (%s) from Bezirk %s added to %s",
                                        mail, mail_type, counter, filename_mails)
                checkpoint.mark_done(url_clubsite)
        checkpoint.close()
        logger.info("%s returned", filename_mails)

    def encode_mail(self, mail, url=None):
        mail = mail.strip()
        mail = mail.replace("encodeEmail(", "")
        mail = mail.replace(")", "")
        mail = mail.replace("'", "")
        mail_splitted = mail.split(",")
        if len(mail_splitted) != 4:
            logger.warning("Unexpected encodeEmail payload '%s' at %s. Skipping...", mail, url)
            return None
        top_level_domain = mail_splitted[0].strip()
        m1 = mail_splitted[1].strip()
        domain = mail_splitted[2].strip()
        m2 = mail_splitted[3].strip()
        delimiter1 = "@"
        delimiter2 = "."
        if m2 != "":
            concat_string = m1 + delimiter2 + m2 + delimiter1 + domain + delimiter2 + top_level_domain
        else:
            concat_string = m1 + delimiter1 + domain + delimiter2 + top_level_domain
        return concat_string.strip()
