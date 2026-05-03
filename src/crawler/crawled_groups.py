import csv
from urllib.parse import urljoin
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from src import helper

TERMINAL = helper.Terminal()


class CrawledGroups:

    def __init__(self, url):
        self.url = url
        TERMINAL.print("initialized CrawledGroups")

    def fetch(self, counter):
        c = 1
        r = requests.get(self.url)
        doc = BeautifulSoup(r.text, "html.parser")
        table = doc.select_one(".result-set")
        links = table.find_all("a")
        filename = f"./Excelfiles/01_Gruppen_Bezirk_{counter}.csv"
        check_file = Path(filename)
        if check_file.is_file():
            TERMINAL.print(f"File {filename} does already exist")
        else:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                TERMINAL.print(f"{filename} created")
                writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                for link in links:
                    url_link = urljoin(self.url, link.attrs["href"])
                    writer.writerow([url_link])
                    TERMINAL.print(f"{link.text} added to {filename}")
                    c = c + 1
            TERMINAL.print(f"{filename} returned")
        return filename
