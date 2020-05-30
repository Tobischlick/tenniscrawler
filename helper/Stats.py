import helper
from pathlib import Path
import csv

Terminal = helper.Terminal()


class Stats:
    def __init__(self):
        self.filepath = f"./Excelfiles/05_Statistik.csv"

    def write_Groups(self, bezirk, counter):
        if self.check_file():
            Terminal.print(f"File {self.filepath} does already exist")
        else:
            with open(self.filepath, "a", newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='|')
                Terminal.print(f"File {self.filepath} created")
                writer.writerow([bezirk, counter])

    def write_Teams(self):
        pass

    def write_Clubs(self):
        pass

    def write_Mails(self):
        pass

    def check_file(self):
        checkfile = Path(self.filepath)
        if checkfile.is_file():
            return True
        else:
            return False
