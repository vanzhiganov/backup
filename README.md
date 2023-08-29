backup
======

src
    files
    pgsql
    mysql

dst
    ftp
    webdav
    s3



Current version: v1.1.6

collection backup and recovery scripts

## Features

* backup files
* backup mysql databases
* backup pgsql databases
* compress archives
* upload archives to webdav storage
* upload archives to ftp server

## Tested

* CentOS 6.6 Server
* Fedora Linux 21 Desktop
* Ubuntu 14.04 LTS Server

# Install

`sudo apt-get install gnupg python-gnupg python-configparser python-easywebdav rng-tools`

`sudo pip install ftptool`


## For Postgresql

`createuser <backup_username>`

`alter user <backup_username> password '<password>';`


`GRANT SELECT ON ALL TABLES IN SCHEMA public TO <backup_usermame>;`

`GRANT CONNECT ON DATABASE <database_name> to <backup_usermame>;`

`GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO <backup_usermame>;`


for pg_basebackup (EXPERIMENTAL)

pg_hba.conf
`local   replication     postgres                                md5`

postgresql.conf
`max_wal_senders = 1`
`wal_level = hot_standby`


# Using

## Examples

Show help

`python backup.py --help`

Specify config file

`python backup.py -c config.ini`

Specify log file

`python backup.py -l backup.log`

# Configuring

## config file example

### 'default' section example

```
[DEFAULT]
InstanceName = WorkPCUbuntuLinux
StorageLocal = /tmp/storage
Compression = yes
CompressionLevel = 9
```

### example files backup

```
[File:test]
Enabled = yes
Directory = /etc
Compression = yes
CompressionLevel = 9
SavedDaily = 7
SavedWeekly = 4
SavedMonthly = 12
Remote = webdav_yandex
SaveLocal = yes
```

### example mysql database backup

```
[Database:mysql_testdatabase]
Enabled = yes
Engine = mysql
Host = localhost
User = root
Password = rootpassword
Database = test_database
Compression = yes
CompressionLevel = 9
SavedDaily = 7
SavedWeekly = 4
SavedMonthly = 12
SaveLocal = no
```

### example postgresql database backup

```
[Database:test_pgsql]
Enabled = yes
Engine = pgsql
Host = localhost
User = backup_user
Password = BacK8OLpU@r
Database = myappdatabase
Remote = webdav_yandex
```

### example webdav config

```
[REMOTE:webdav_yandex]
Type = webdav
Host = webdav.yandex.ru
Port = 443
Protocol = https
Login = user
Password = password
```

# GPG keys and crypt

## Prepare GPG keys

`gpg --gen-key`

Make few steps and gpg-key will be generated

In the next step we need to change trust level for user,

`gpg --sign-key email@address.com`

After that you fully trust the key.

### Trusting levels

    1 = I don't know or won't say
    2 = I do NOT trust
    3 = I trust marginally
    4 = I trust fully
    5 = I trust ultimately

## Decrypt archive

`gpg -r email@address.com --decrypt-files WorkPCUbuntuLinux_test_20141107.tar.gpg`
