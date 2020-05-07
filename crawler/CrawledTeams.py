import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import helper

Terminal = helper.Terminal()


class CrawledTeams:
    def __init__(self, filepath):
        self.filepath = filepath
        Terminal.print("initialized 'CrawledTeams'")

    def fetch(self, counter):
        filename = f"02_Mannschaften_Bezirk_{counter}.csv"
        checkFile = Path(filename)
        if checkFile.is_file():
            Terminal.print("File " + filename + " does already exist")
        else:
            with open(filename, "w", newline="") as csvfile:
                Terminal.print(filename + " created")
                with open(self.filepath, newline="") as csvfile_read:
                    Terminal.print("read file: " + self.filepath)
                    reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                    for row in reader:
                        urlLeague = ' '.join(row)
                        r = requests.get(urlLeague)
                        doc = BeautifulSoup(r.text, "html.parser")
                        table = doc.select_one(".result-set")
                        links = table.find_all("a")
                        writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                        for link in links:
                            url_link = urljoin(urlLeague, link.attrs["href"])
                            writer.writerow([url_link])
                            Terminal.print(link.text + " added to " + filename)
            Terminal.print(filename + " returned")
        return filename