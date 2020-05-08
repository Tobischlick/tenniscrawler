import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import helper

Terminal = helper.Terminal()


class CrawledGroups:

    def __init__(self, url):
        self.url = url
        Terminal.print("initialized CrawledGroups")

    def fetch(self, counter):
        r = requests.get(self.url)
        doc = BeautifulSoup(r.text, "html.parser")
        table = doc.select_one(".result-set")
        links = table.find_all("a")
        filename = f"./Excelfiles/01_Gruppen_Bezirk_{counter}.csv"
        checkFile = Path(filename)
        if checkFile.is_file():
            Terminal.print("File " + filename + " does already exist")
        else:
            with open(filename, "w", newline="") as csvfile:
                Terminal.print(filename + " created")
                writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                for link in links:
                    url_link = urljoin(self.url, link.attrs["href"])
                    writer.writerow([url_link])
                    Terminal.print(link.text + " added to " + filename)
            Terminal.print(filename + " returned")
        return filename
