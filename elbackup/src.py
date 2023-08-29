"""Source module"""

import os


def BackupFiles(source):
    pass


def BackupMysql(host, user, password, database, destination):
    shell = '/usr/bin/mysqldump -h %(host)s -u%(user)s --password=%(password)s %(database)s > %(destination)s' % {
        "host": host,
        "user": user,
        "password": password,
        "database": database,
        "destination": destination
    }
    os.system(shell)


def BackupPgsql(host, user, password, database, destination):
    shell = """PGPASSWORD="%(password)s" pg_dump -h %(host)s -U%(user)s %(database)s > %(destination)s""" % {
        "host": host,
        "user": user,
        "password": password,
        "database": database,
        "destination": destination,
    }
    os.system(shell)
