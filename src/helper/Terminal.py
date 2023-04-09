from datetime import datetime


class Terminal:
    def __init__(self):
        pass

    def print(self, message):
        new_message = datetime.now().strftime("%d.%m.%y - %H:%M:%S -> ") + message
        print(new_message)
        self.log(new_message)

    def log(self, new_message):
        date = datetime.now().strftime("%d.%m.%y")
        logfile = f"./Logfiles/{date}_log.txt"
        with open(logfile, "a") as log:
            log.write(new_message + "\n")