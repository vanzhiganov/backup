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

```
[DEFAULT]
StorageLocal = /tmp/storage
Compression = yes
CompressionLevel = 9

[File:test]
Enabled = yes
Directory = /etc
Compression = yes
CompressionLevel = 9
SavedDaily = 7
SavedWeekly = 4
SavedMonthly = 12

[Database:test]
Enabled = yes
Engine = mysql
Host = localhost
User = root
Password = rootpassword
Compression = yes
CompressionLevel = 9
SavedDaily = 7
SavedWeekly = 4
SavedMonthly = 12
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
