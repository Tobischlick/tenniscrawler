import csv
from urllib.parse import urljoin
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from src import helper

TERMINAL = helper.Terminal()


class CrawledClubs:

    def __init__(self, filepath):
        self.filepath = filepath
        TERMINAL.print("initialized 'CrawledClubs'")

    def fetch(self, counter):
        c = 1
        filename = f"./Excelfiles/03_Clubs_Bezirk_{counter}.csv"
        check_file = Path(filename)
        if check_file.is_file():
            TERMINAL.print(f"File {filename} does already exist")
        else:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                TERMINAL.print(f"{filename} created")
                with open(self.filepath, newline="", encoding="utf-8") as csvfile_read:
                    TERMINAL.print(f"read file: {self.filepath}")
                    reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                    writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                    for row in reader:
                        club_url = ' '.join(row)
                        r = requests.get(club_url)
                        doc = BeautifulSoup(r.text, "html.parser")
                        table = doc.select_one(".result-set")

                        if table is None:
                            TERMINAL.print(f"Warning: Could not find table at {club_url}. Skipping...")
                            continue

                        links = table.find_all("a")
                        club = links[0].text.strip()
                        urlsite = urljoin(club_url, links[0].attrs["href"])
                        writer.writerow([urlsite])
                        TERMINAL.print(f"{club} added to {filename}")
                        c = c + 1
            TERMINAL.print(f"{filename} returned")
        return filename
