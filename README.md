backup
======

collection backup and recovery scripts

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
