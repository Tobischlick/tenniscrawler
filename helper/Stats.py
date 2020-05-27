import helper

Terminal = helper.Terminal()

class Stats:
    def __init__(self):
        self.filepath = f"05_Statistik"

    def write_Groups(self, bezirk, counter):
        Terminal.print(f"{bezirk} - {counter}")

    def write_Teams(self):
        pass

    def write_Clubs(self):
        pass

    def write_Mails(self):
        pass