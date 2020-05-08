import csv
import helper


class DeleteDuplicates:

    def __init__(self):
        Terminal = helper.Terminal()
        Terminal.print("initialized 'DeleteDuplicates'")

    def delete(self, filename):
        Terminal = helper.Terminal()
        Terminal.print(f"{filename} will be checked for duplicates")
        list_old = []
        with open(filename, "r", newline="") as csvfile_read:
            reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
            for row in reader:
                list_old.append(' '.join(row))
        Terminal.print("old list: " + str(len(list_old)))
        list_new = list(dict.fromkeys(list_old))
        Terminal.print("new list: " + str(len(list_new)))
        diff = len(list_old) - len(list_new)
        if diff > 0:
            with open(filename, "w", newline="") as csvfile_write:
                writer = csv.writer(csvfile_write, delimiter=';', quotechar='|')
                for item in list_new:
                    writer.writerow([item])
                Terminal.print(str(diff) + " items deleted duplicates out of: " + filename)
        else:
            Terminal.print(f"no duplicates found in {filename}")
