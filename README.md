backup
======

collection backup and recovery scripts

Using
-----

**backupfiles.py**

Для архивации файлов необходимо создать файл *toBackup.ls* в котором необходимо перечислить директории и файлы для архивации, например:

    /var/www
    /home

После сохранения можно запустить скрипт:

    python backupfiles.py
