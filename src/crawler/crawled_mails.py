import configparser
import csv
import requests
from bs4 import BeautifulSoup
from src import helper

TERMINAL = helper.Terminal()


class CrawledMails:
    def __init__(self, filepath):
        self.filepath = filepath
        TERMINAL.print("initialized CrawledMails")

    def fetch(self, counter, filename_mails):
        config = configparser.ConfigParser()
        config.read('.config/config.ini')
        mails_config = dict(config['MAILS'])

        with open(filename_mails, "a", newline="", encoding="utf-8") as csvfile:
            TERMINAL.print(f"{filename_mails} created")
            with open(self.filepath, newline="", encoding="utf-8") as csvfile_read:
                TERMINAL.print(f"read file: {self.filepath}")
                reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                writer.writerow(['Position', 'E-Mail', 'Bezirk'])
                for row in reader:
                    url_clubsite = ' '.join(row)
                    r = requests.get(url_clubsite)
                    doc = BeautifulSoup(r.text, "html.parser")
                    finder = doc.find_all("td")
                    for i in range(0, len(finder)):
                        mail_type = finder[i].text
                        for mail_pattern in mails_config.values():
                            if mail_type == mail_pattern:
                                mail_string = finder[i + 3].string
                                if mail_string != "-" and mail_string != "":
                                    mail = self.encode_mail(mail_string)
                                    writer.writerow([mail_type, mail, counter])
                                    TERMINAL.print(
                                        f"Mail '{mail}' ({mail_type}) from Bezirk {counter} added to {filename_mails}")
        TERMINAL.print(f"{filename_mails} returned")

    def encode_mail(self, mail):
        mail = mail.strip()
        mail = mail.replace("encodeEmail(", "")
        mail = mail.replace(")", "")
        mail = mail.replace("'", "")
        mail_splitted = mail.split(",")
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
