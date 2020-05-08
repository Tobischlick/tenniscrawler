import requests
import helper
import csv
from bs4 import BeautifulSoup

Terminal = helper.Terminal()


class CrawledMails:
    def __init__(self, filepath):
        self.filepath = filepath
        Terminal.print("initialized CrawledMails")

    def fetch(self, counter):
        filename_jugend = f"04_Jugendleiter_Bezirk_{counter}.csv"
        filename_sport = f"04_SportlicheLeiter_Bezirk_{counter}.csv"
        filename_mannschaft = f"04_Mannschaftsführer_Bezirk{counter}.csv"
        with open(self.filepath, newline="") as csvfile_read:
            Terminal.print("read file: " + self.filepath)
            reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
            for row in reader:
                urlCLubsite = ' '.join(row)
                r = requests.get(urlCLubsite)
                doc = BeautifulSoup(r.text, "html.parser")
                table = doc.select(".result-set")[2]
                print(table)
                break
