import csv
from src import helper


class DeleteDuplicates:

    def __init__(self):
        terminal = helper.Terminal()
        terminal.print("initialized 'DeleteDuplicates'")

    def delete(self, filename):
        terminal = helper.Terminal()
        terminal.print(f"{filename} will be checked for duplicates")
        list_old = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile_read:
            reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
            for row in reader:
                list_old.append(' '.join(row))
        terminal.print("old list: " + str(len(list_old)))
        list_new = list(dict.fromkeys(list_old))
        terminal.print("new list: " + str(len(list_new)))
        diff = len(list_old) - len(list_new)
        if diff > 0:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile_write:
                writer = csv.writer(csvfile_write, delimiter=';', quotechar='|')
                for item in list_new:
                    writer.writerow([item])
                terminal.print(str(diff) + " items deleted duplicates out of: " + filename)
        else:
            terminal.print(f"no duplicates found in {filename}")
