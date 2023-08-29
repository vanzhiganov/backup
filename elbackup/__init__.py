import os
import datetime
import zipfile
import glob
import logging


class File:
    def __init__(self, source, destination, stored_copies=7):
        date_format = [
            "%A %d.%m.%Y",
            "%Y%m%d"
        ]

        default_date_format = 1

        now_date = datetime.date.today()
        self.name = now_date.strftime(date_format[default_date_format]) + '.zip'

        self.source_files = []
        self.source = source
        self.destination = ""

        self.get_list_files(source)
        self.backup()

    def get_list_files(self, directory):
        """
        Get file in subfolders
        """
        try:
            for file in os.listdir(directory):

                path = os.path.join(directory, file)
                print (path)
                if not os.path.isdir(path):
                    self.source_files.append(path)
                else:
                    self.get_list_files(path)
        except:
            return None

        # return self.source_files

    def backup(self):
        logging.warning("Files are being archived...")

        filename = os.path.join(self.destination, self.name)

        with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED) as bak:
            for line in self.source_files:
                try:
                    bak.write(line)
                    # logging.info(("Add file %s into %s" % (l, elbackup.filename)).decode('utf-8'))
                except:
                    logging.error("Error: file adding fail %s %s" % (line, bak.filename))
            bak.close()
        logging.info("Archiving completed")
