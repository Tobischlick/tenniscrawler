import requests
import helper
import csv
from bs4 import BeautifulSoup
from pathlib import Path

Terminal = helper.Terminal()


class CrawledMails:
    def __init__(self, filepath):
        self.filepath = filepath
        Terminal.print("initialized CrawledMails")

    def fetch(self, counter, filename_mails):
        with open(filename_mails, "a", newline="") as csvfile:
            Terminal.print(f"{filename_mails} created")
            with open(self.filepath, newline="") as csvfile_read:
                Terminal.print(f"read file: {self.filepath}")
                reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                writer.writerow(['Position', 'E-Mail', 'Bezirk'])
                for row in reader:
                    urlCLubsite = ' '.join(row)
                    r = requests.get(urlCLubsite)
                    doc = BeautifulSoup(r.text, "html.parser")
                    finder = doc.find_all("td")
                    for i in range(0, len(finder)):
                        mail_type = finder[i].text
                        if mail_type == "Sportwart/in" or mail_type == "Jugendwart/in" or mail_type == "Mannschaftsfuehrer/in":
                            mail_string = finder[i + 3].text
                            if mail_string != "-":
                                mail = self.encode_mail(mail_string)
                                writer.writerow([mail_type, mail, counter])
                                Terminal.print(f"Mail '{mail}' added to {filename_mails}")
        Terminal.print(f"{filename_mails} returned")

    def encode_mail(self, mail):
        mail = mail.strip()
        mail = mail.replace("encodeEmail(", "")
        mail = mail.replace(")", "")
        mail = mail.replace("'", "")
        mail_splitted = mail.split(",")
        topLevelDomain = mail_splitted[0].strip()
        m1 = mail_splitted[1].strip()
        domain = mail_splitted[2].strip()
        m2 = mail_splitted[3].strip()
        delimiter1 = "@"
        delimiter2 = "."
        if m2 != "":
            concatString = m1 + delimiter2 + m2 + delimiter1 + domain + delimiter2 + topLevelDomain
        else:
            concatString = m1 + delimiter1 + domain + delimiter2 + topLevelDomain
        return concatString.strip()
