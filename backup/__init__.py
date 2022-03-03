#!/usr/bin/env python
# -*- coding: utf-8 -*-

# file: __init__.py
import os, datetime, zipfile, glob, logging


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
        # logging.warning(('Выполняется архивация файлов...').decode('utf-8'))
        with zipfile.ZipFile(os.path.join(self.destination, self.name), 'w', compression=zipfile.ZIP_DEFLATED) as backup:
            for l in self.source_files:
                try:
                    backup.write(l)
                    # logging.info(("Add file %s into %s" % (l, backup.filename)).decode('utf-8'))
                except:
                    # logging.error(("Ошибка добавления файла: %s в архив %s" % (l, backup.filename)).decode('utf-8'))
                    logging.error("Error: file adding fail %s %s" % (l, backup.filename))

            backup.close
            logging.warning(('Архивация завершена').decode('utf-8'))


class Database:
	def __init__(self):
