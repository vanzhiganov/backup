#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, datetime, zipfile, glob, logging

#Текущее дата/время
curr_date = datetime.datetime.today()
#Текущая дата(используется для формирования имени архива)
now_date = datetime.date.today()
#Список того что будет архивироваться
FilesToBackup = ['/home/vanzhiganov/test']
#Что необдохимо архивировать
toBackup = os.path.join(os.path.curdir, 'toBackup.ls')
#Куда необходимо архивировать
backupTo = "/var/backups"
#Формируем имя архива
BackupName = now_date.strftime("%A %d.%m.%Y") + '.zip'
#Формируем имя Лог файла
BackupLog = now_date.strftime("%A %d.%m.%Y") + '.log'
#Сколько дней хранить архивы
StoreBackupCopy = 7

logging.basicConfig(format = u'[%(asctime)s] %(levelname)-8s  %(message)s',
#                    level = logging.DEBUG,
                    filename = os.path.join(backupTo,BackupLog))

#Получаем корневые директории для архивирования
def GetSrcList(file):
    SrcLs = []
    with open(file) as f:
        SrcLs = f.read().splitlines()
    return SrcLs

#Функция заполняет список для архивирования
def GetListForBackup(PathForBackup):
    for file in os.listdir(PathForBackup):
        path = os.path.join(PathForBackup, file)
        if not os.path.isdir(path):
            FilesToBackup.append(path)
        else:
            GetListForBackup(path)

#Функция удаляет архивы старше определенной даты
def DelOldBackup():
   backupLs = glob.glob(os.path.join(backupTo, "*.*"))
   for ls in backupLs:
       fLastChange = datetime.datetime.fromtimestamp(os.path.getmtime(ls))
       PassDay = curr_date-fLastChange
       if PassDay.days > StoreBackupCopy:
            try:
                logging.warning(('Удаляем файлы старше: %s дней' % StoreBackupCopy).decode('utf-8'))
                os.remove(ls)
                logging.warning(('Файл %s был удален' % ls).decode('utf-8'))
            except:
                logging.error(('Ошибка удаления файла %s' % ls).decode('utf-8'))

def backup(list_backup):
    logging.warning(('Выполняется архивация файлов...').decode('utf-8'))
    with zipfile.ZipFile(os.path.join(backupTo, BackupName), 'w', compression=zipfile.ZIP_DEFLATED) as Backup:
        for l in list_backup:
            try:
                Backup.write(l)
                logging.info(("Добавляем файл %s в архив %s" % (l, Backup.filename)).decode('utf-8'))
            except:
                logging.error(("Ошибка добавления файла: %s в архив %s" % (l, Backup.filename)).decode('utf-8'))

        Backup.close
        logging.warning(('Архивация завершена').decode('utf-8'))

logging.warning(('Заполняем список для архивирования абсолютными путями файлов').decode('utf-8'))

for c in GetSrcList(toBackup):
    GetListForBackup(c)

backup(FilesToBackup)
DelOldBackup()
