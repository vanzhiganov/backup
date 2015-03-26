#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
from optparse import OptionParser
import logging
import datetime
import backup
import configparser
import subprocess
import gnupg
import easywebdav

parser = OptionParser()
parser.add_option("-c", "--config", dest="config_filename", default="config.ini", help="read from FILE", metavar="CONFIG")
parser.add_option("-l", "--log", dest="log_filename", default="backup.log", help="write report to FILE", metavar="FILE")
parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

(options, args) = parser.parse_args()

config = configparser.ConfigParser()

# read config file
config.read(options.config_filename)

logging.basicConfig(format=u'[%(asctime)s] %(levelname)-8s  %(message)s', level=logging.DEBUG, filename=options.log_filename)

# GPG
def gpg_gen_key(email, phrase):
    input_data = gpg.gen_key_input(name_email=email, passphrase=phrase)
    return gpg.gen_key(input_data)


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
    logging.info("check exists CompressionLevel: %s [OK]" % config['DEFAULT']['CompressionLevel'])
else:
    logging.error("check exists CompressionLevel: ... [FAIL]")
    logging.info("update %s: add CompressionLevel parameter to DEFAULT section" % options.config_filename)
    sys.exit()

if not os.path.isdir(config['DEFAULT']['StorageLocal']):
    logging.error("check exists local storage folder: %s [FAIL]" % config['DEFAULT']['StorageLocal'])
    sys.exit()


# gpg test
if config['DEFAULT']['Encrypt'] == "yes":
    gpg = gnupg.GPG(gnupghome='gpg')

    gpg_test = True
    if not os.path.isdir("gpg"):
        print "gpg folder not exists"
        gpg_test = False
    else:
        if not os.path.isfile("gpg/pubring.gpg"):
            print "gpg pubring not exists"
            gpg_test = False
        else:
            if not os.path.isfile("gpg/secring.gpg"):
                print "gpg secring not exists"
                gpg_test = False
            else:
                if not os.path.isfile("gpg/trustdb.gpg"):
                    print "gpg trustdb not exists"
                    gpg_test = False

    if not gpg_test:
        input_data = gpg.gen_key_input(name_email=config['DEFAULT']['EncryptEmail'], passphrase=config['DEFAULT']['EncryptPhrase'])
        key = gpg.gen_key(input_data)
        logging.info("new gpg key has generated: %s" % key)


# if (len(config) - 1) <= 0:
    # logging.error("no task to bakcup")
    # sys.exit();

# start backup
for x in config:
    if x == "DEFAULT":
        continue

    if not "Enabled" in config[x]:
        continue

    (datatype, jobname) = x.split(":")

    if datatype == "File":
        if config[x]['Enabled'] == "no":
            continue

        logging.info("Backup files. Job: %s" % jobname)


        date_format = ["%A %d.%m.%Y", "%Y%m%d"]
        default_date_format = 1

        b_date = datetime.date.today().strftime(date_format[default_date_format])

        b_storagelocal = config['DEFAULT']['StorageLocal']
        b_archivename = "%s_%s_%s.tar" % (config['DEFAULT']['InstanceName'], jobname, b_date)
        b_source = config[x]['Directory']
        b_destination = "%s/%s" % (b_storagelocal, b_archivename)

        subprocess.call(['tar', 'cfv', b_destination, b_source])

        if config[x]['Compression'] == "yes":
            subprocess.call(['gzip', b_destination])
            # check exists compresed file
            if os.path.isfile("%s.gz" % b_destination):
                b_destination = "%s.gz" % b_destination
            b_archivename = "%s.gz" % b_archivename


        # gpg --output doc.gpg --symmetric doc
        # gpg -e -r email@address.com WorkPCUbuntuLinux_test_20141107.tar

        # p = subprocess.Popen('tar cfv %s/%s %s' % (b_storagelocal, b_archivename, b_source), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # for line in p.stdout.readlines():
            # print line, retval = p.wait()
        # print p

        if "Remote" in config[x]:
            remote = {}
            remote['name'] = 'REMOTE:%s' % config[x]['Remote']

            if remote['name'] in config:
                remote['type'] = config[remote['name']]['Type']
                remote['host'] = config[remote['name']]['Host']
                remote['port'] = int(config[remote['name']]['Port'])
                remote['protocol'] = config[remote['name']]['Protocol']
                remote['login'] = config[remote['name']]['Login']
                remote['password'] = config[remote['name']]['Password']
                remote['destination'] = "%s/%s/%s" % (config['DEFAULT']['InstanceName'], jobname, b_archivename)

                # connect to webdav
                webdav = easywebdav.connect(remote['host'], port=remote['port'], protocol=remote['protocol'], username=remote['login'], password=remote['password'])
                # todo: check exists folder
                if not webdav.exists(config['DEFAULT']['InstanceName']):
                    webdav.mkdir(config['DEFAULT']['InstanceName'])

                if not webdav.exists(config['DEFAULT']['InstanceName'] + "/" + jobname):
                    webdav.mkdir(config['DEFAULT']['InstanceName']+"/"+jobname)

                # upload archive to webdav
                webdav.upload(b_destination, remote['destination'])

    if datatype == "Database":
        if config[x]['Enabled'] == "no":
            continue

        print "Backup database. Job: %s" % jobname

        date_format = ["%A %d.%m.%Y", "%Y%m%d"]
        default_date_format = 1

        b_storagelocal = config['DEFAULT']['StorageLocal']
        b_date = datetime.date.today().strftime(date_format[default_date_format])
        b_archivename = "%s_%s_%s_%s.sql" % (config['DEFAULT']['InstanceName'], config[x]['Engine'], config[x]['Database'], b_date)
        b_destination = "%s/%s" % (b_storagelocal, b_archivename)

        if config[x]['Engine'] == "mysql":
            mc = {
                "host": config[x]['Host'],
                "user": config[x]['User'],
                "password": config[x]['Password'],
                "database": config[x]['Database'],
                "destination": b_destination
            }
            cmd = '/usr/bin/mysqldump -h %(host)s -u%(user)s --password=%(password)s %(database)s > %(destination)s' % mc
            os.system(cmd)
        elif config[x]['Engine'] == "mysql":
            pc = {
                "user": config[x]['User'],
                "password": config[x]['Password'],
                "host": config[x]['Host'],
                "database": config[x]['Database'],
                "destination": b_destination,
            }

            cmd = """PGPASSWORD="%(password)s"; pg_dump -h %(host)s -U%(user)s %(database)s > %(destination)s""" % pc
            os.system(cmd)
        else:
            continue

        if config[x]['Compression'] == "yes":
            subprocess.call(['gzip', b_destination])
            b_destination = "%s.gz" % b_destination
            
        if "Remote" in config[x]:
            remote = {}
            remote['name'] = 'REMOTE:%s' % config[x]['Remote']

            if remote['name'] in config:
                remote['type'] = config[remote['name']]['Type']
                remote['host'] = config[remote['name']]['Host']
                remote['port'] = int(config[remote['name']]['Port'])
                remote['protocol'] = config[remote['name']]['Protocol']
                remote['login'] = config[remote['name']]['Login']
                remote['password'] = config[remote['name']]['Password']
                remote['destination'] = "%s/%s/%s" % (config['DEFAULT']['InstanceName'], jobname, b_archivename)

                # connect to webdav
                webdav = easywebdav.connect(remote['host'], port=remote['port'], protocol=remote['protocol'], username=remote['login'], password=remote['password'])
                # todo: check exists folder
                if not webdav.exists(config['DEFAULT']['InstanceName']):
                    webdav.mkdir(config['DEFAULT']['InstanceName'])

                if not webdav.exists(config['DEFAULT']['InstanceName'] + "/" + jobname):
                    webdav.mkdir(config['DEFAULT']['InstanceName']+"/"+jobname)

                # upload archive to webdav
                webdav.upload(b_destination, remote['destination'])

#
#
# # if __name__ == '__main__':
#     # backup.backup().main()
