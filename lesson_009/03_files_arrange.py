# -*- coding: utf-8 -*-

import os, time, shutil, zipfile


# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.


class Sorter:

    def __init__(self, source_path, destination_dir_name):
        self.source_path = os.path.normpath(source_path)
        self.destination_dir_name = destination_dir_name

    def _get_destination_dir_path(self, *subdirs):
        source_dir_parent_path = os.path.dirname(self.source_path)
        destination_dir_path = os.path.join(source_dir_parent_path, destination_dir_name, *subdirs)
        return destination_dir_path


class FileSorter(Sorter):

    def _get_file_creation_data(self, file_path):
        file_created_secs = os.path.getctime(file_path)
        file_created_time = time.gmtime(file_created_secs)
        year = str(file_created_time.tm_year)
        month = str(file_created_time.tm_mon).zfill(2)
        return year, month

    def sort_by_date(self):
        for dir_path, dir_names, file_names in os.walk(self.source_path):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                year, month = self._get_file_creation_data(file_path)
                new_dir_path = self._get_destination_dir_path(year, month)
                os.makedirs(new_dir_path, exist_ok=True)
                shutil.copy2(file_path, new_dir_path)


source_dir_path = r'C:\Users\User\Downloads\[Вадим Шандринов] Python-разработчик\9. Работа с файлами и форматированный ' \
                  'вывод\lesson_009\icons'
destination_dir_name = 'icons_by_year'
FileSorter(source_dir_path, destination_dir_name).sort_by_date()


class ZipSorter(Sorter):

    def _get_file_creation_data(self, zfile, member):
        file_time = zfile.getinfo(member).date_time
        year = str(file_time[0])
        month = str(file_time[1]).zfill(2)
        return year, month

    def sort_by_date(self):
        zfile = zipfile.ZipFile(self.source_path, 'r')
        for member in zfile.namelist():
            file_name = os.path.basename(member)
            if file_name:
                year, month = self._get_file_creation_data(zfile, member)
                new_dir_path = self._get_destination_dir_path(year, month)
                os.makedirs(new_dir_path, exist_ok=True)
                with zfile.open(member) as source_file, open(os.path.join(new_dir_path, file_name), "wb") as new_file:
                    shutil.copyfileobj(source_file, new_file)
        zfile.close()


zip_file_path = r'C:\Users\User\Downloads\[Вадим Шандринов] Python-разработчик\9. Работа с файлами и форматированный вывод\lesson_009\icons.zip'
destination_dir_name = 'icons_by_year_zip'
ZipSorter(zip_file_path, destination_dir_name).sort_by_date()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Основная функция должна брать параметром имя zip-файла и имя целевой папки.
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
