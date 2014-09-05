#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
from optparse import OptionParser
import logging
import backup
import configparser

# logging.basicConfig(format=u'[%(asctime)s] %(levelname)-8s  %(message)s', level=logging.DEBUG, filename=os.path.join(backupTo,BackupLog))

parser = OptionParser()

# parser.add_option("-o", "--object", dest="object_name", help="enter fs or db", metavar="OBJECT")
parser.add_option("-c", "--config", dest="config_filename", default="config.ini", help="read from FILE", metavar="CONFIG")

parser.add_option("-l", "--log", dest="log_filename", default="backup.log", help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

(options, args) = parser.parse_args()

# print options.config_filename

config = configparser.ConfigParser()
config.read(options.config_filename)
# print config.sections()

print config['DEFAULT']['StorageLocal']

for x in config:
	if x == "DEFAULT":
		continue

	if not "Enabled" in config[x]:
		continue

	(datatype, jobname) = x.split(":")

	if datatype == "File":
		print "Backup files. Job: %s" % jobname
 		# print x.split(":")[1]
 		# print config[x]['Directory']

 		do = backup.File(config[x]['Directory'], "%s/%s" % (config['DEFAULT']['StorageLocal'], jobname))

	# if datatype == "Database":
		# print "Backup database. Job: %s" % jobname


# if __name__ == '__main__':
    # backup.backup().main()