backup
======

collection backup and recovery scripts

## features

* backup files
* backup mysql databases
* compress archives
* upload archives to webdav storage


# Install

`sudo apt-get install gnupg`

`sudo apt-get install rng-tools`

`sudo pip install configparser`

`sudo pip install python-gnupg`

`sudo pip install easywebdav`


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
