import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import helper

Terminal = helper.Terminal()


class CrawledClubs:

    def __init__(self, filepath):
        self.filepath = filepath
        Terminal.print("initialized 'CrawledClubs'")

    def fetch(self, counter):
        c = 1
        filename = f"./Excelfiles/03_Clubs_Bezirk_{counter}.csv"
        checkFile = Path(filename)
        if checkFile.is_file():
            Terminal.print(f"File {filename} does already exist")
        else:
            with open(filename, "w", newline="") as csvfile:
                Terminal.print(f"{filename} created")
                with open(self.filepath, newline="") as csvfile_read:
                    Terminal.print(f"read file: {self.filepath}")
                    reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                    writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                    for row in reader:
                        club_url = ' '.join(row)
                        r = requests.get(club_url)
                        doc = BeautifulSoup(r.text, "html.parser")
                        table = doc.select_one(".result-set")
                        links = table.find_all("a")
                        club = links[0].text.strip()
                        urlsite = urljoin(club_url, links[0].attrs["href"])
                        writer.writerow([urlsite])
                        Terminal.print(f"{club} added to {filename}")
                        c = c + 1
            Terminal.print(f"{filename} returned")
        return filename
