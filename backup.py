#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
from optparse import OptionParser
import logging
import backup
import configparser

logging.basicConfig(format=u'[%(asctime)s] %(levelname)-8s  %(message)s', level=logging.DEBUG, filename="/var/log/backup.log")

parser = OptionParser()
parser.add_option("-c", "--config", dest="config_filename", default="config.ini", help="read from FILE", metavar="CONFIG")
parser.add_option("-l", "--log", dest="log_filename", default="backup.log", help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

(options, args) = parser.parse_args()

config = configparser.ConfigParser()

# read config file
config.read(options.config_filename)

# print config.sections()
# print config['DEFAULT']['StorageLocal']
# print config.sections()

# TODO: check exists need folders
logging.info("check system")

if "StorageLocal" in config['DEFAULT']:
	logging.info("check exists StorageLocal: %s [OK]" % config['DEFAULT']['StorageLocal'])
else:
	logging.error("check exists StorageLocal: ... [FAIL]")
	logging.info("update %s: add StorageLocal parameter to DEFAULT section" % options.config_filename)
	sys.exit()

if "Compression" in config['DEFAULT']:
	logging.info("check exists Compression: %s [OK]" % config['DEFAULT']['Compression'])
else:
	logging.error("check exists Compression: ... [FAIL]")
	logging.info("update %s: add Compression parameter to DEFAULT section" % options.config_filename)
	sys.exit()

if "CompressionLevel" in config['DEFAULT']:
	logging.info("check exists CompressionLevel: %s" % config['DEFAULT']['StorageLocal'])
else:
	logging.error("check exists CompressionLevel: ... [FAIL]")
	logging.info("update %s: add CompressionLevel parameter to DEFAULT section" % options.config_filename)
	sys.exit()



for x in config:
	print x
# 	if x == "DEFAULT":
# 		continue
#
# 	if not "Enabled" in config[x]:
# 		continue
#
# 	(datatype, jobname) = x.split(":")
#
# 	if datatype == "File":
# 		print "Backup files. Job: %s" % jobname
#  		# print x.split(":")[1]
#  		# print config[x]['Directory']
#
#  		do = backup.File(config[x]['Directory'], "%s/%s" % (config['DEFAULT']['StorageLocal'], jobname))
#
# 	# if datatype == "Database":
# 		# print "Backup database. Job: %s" % jobname
#
#
# # if __name__ == '__main__':
#     # backup.backup().main()
