import csv
from urllib.parse import urljoin
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from src import helper

TERMINAL = helper.Terminal()


class CrawledTeams:
    def __init__(self, filepath):
        self.filepath = filepath
        TERMINAL.print("initialized 'CrawledTeams'")

    def fetch(self, counter):
        filename = f"./Excelfiles/02_Mannschaften_Bezirk_{counter}.csv"
        check_file = Path(filename)
        if check_file.is_file():
            TERMINAL.print(f"File {filename} does already exist")
        else:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                TERMINAL.print(f"{filename} created")
                with open(self.filepath, newline="", encoding="utf-8") as csvfile_read:
                    TERMINAL.print(f"read file: {self.filepath}")
                    reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
                    for row in reader:
                        url_league = ' '.join(row)
                        r = requests.get(url_league)
                        doc = BeautifulSoup(r.text, "html.parser")
                        table = doc.select_one(".result-set")

                        if table is None:
                            TERMINAL.print(f"Warning: Could not find table at {url_league}. Skipping...")
                            continue

                        links = table.find_all("a")
                        writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                        for link in links:
                            url_link = urljoin(url_league, link.attrs["href"])
                            writer.writerow([url_link])
                            TERMINAL.print(f"{link.text} added to {filename}")
            TERMINAL.print(f"{filename} returned")
        return filename
