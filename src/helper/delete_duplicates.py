import csv
import logging

logger = logging.getLogger(__name__)


class DeleteDuplicates:

    def __init__(self):
        logger.info("initialized 'DeleteDuplicates'")

    def delete(self, filename):
        logger.info("%s will be checked for duplicates", filename)
        list_old = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile_read:
            reader = csv.reader(csvfile_read, delimiter=';', quotechar='|')
            for row in reader:
                list_old.append(' '.join(row))
        logger.info("old list: %s", len(list_old))
        list_new = list(dict.fromkeys(list_old))
        logger.info("new list: %s", len(list_new))
        diff = len(list_old) - len(list_new)
        if diff > 0:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile_write:
                writer = csv.writer(csvfile_write, delimiter=';', quotechar='|')
                for item in list_new:
                    writer.writerow([item])
                logger.info("%s items deleted duplicates out of: %s", diff, filename)
        else:
            logger.info("no duplicates found in %s", filename)
