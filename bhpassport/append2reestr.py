# Выдергивает из TeX - файла с паспортом скважины параметры скважины и формирует строку для вставки
# в XLS-файл с реестром скважин. Строка также заносится в clipboard

import re
import subprocess
import os
import datetime


FILENAME = 'bhpassport.tex'             # Имя TeX - файла с паспортом скважины

REESTR_FILE_NAME = 'D:\\OneDrive\\_Реестр скважин\\Реестр скважин.xlsx'

if not os.path.exists(REESTR_FILE_NAME):
    REESTR_FILE_NAME = 'D:\\SkyDrive\\_Реестр скважин\\Реестр скважин.xlsx'


pattern1 = re.compile(r'{(\d*.\d*)}')     # Шаблон 1
pattern2 = re.compile(r'.*{.*}{(.*)}')   # Шаблон 2


# Копирует строку txt в буфер обмена (работает в Windows)
def copy2clip(txt):
   cmd='echo '+txt.strip()+'|clip'
   return subprocess.check_call(cmd, shell=True)


with open(FILENAME, encoding='utf-8') as file:
    content = file.readlines()


for line in content:
    # print(line.strip())
    # Depth
    if re.search(r'.*\\newcommand{\\txtDepth}', line):
        # print(line.strip())
        Depth = pattern1.findall(line)[0].replace('.', ',')
    # Debit
    if re.search(r'.*\\newcommand{\\txtDebit}', line):
        # print(line.strip())
        Debit = pattern1.findall(line)[0].replace('.', ',')
    # Coordinates
    if re.search(r'.*\\newcommand{\\txtCoords}', line):
        # print(line.strip())
        Coordinates = pattern2.findall(line)[0]
    # Сadaster
    if re.search(r'.*\\newcommand{\\txtCadaster}', line):
        # print(line.strip())
        Cadaster = pattern2.findall(line)[0]
    # Address
    if re.search(r'.*\\newcommand{\\txtAddress}', line):
        # print(line.strip())
        Address = pattern2.findall(line)[0]

print('Depth    : {}'.format(Depth))
print('Debit    : {}'.format(Debit))
print('Coords   : {}'.format(Coordinates))

(lat, lon) = Coordinates.split()
print('Lat      : {}'.format(lat))
print('Lon      : {}'.format(lon))

print('Cadaster : {}'.format(Cadaster))
print('Address  : {}'.format(Address))

full_path = '{}\{}'.format(os.getcwd(), FILENAME)
now = datetime.datetime.now()
curr_date = '{:02d}.{:02d}.{}'.format(now.day, now.month, now.year)

# Заменим символы << и >> на кавычки
Address = Address.replace('<<', '"')
Address = Address.replace('>>', '"')

res = '0\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
    curr_date, Address, Address, Cadaster, lat, lon, 0, Depth, Debit, full_path)

print(res)
copy2clip(res)
print('\n Результат скопирован в буфер обмена ')

# Запустим Excel и откроем файл с реестром скважин
subprocess.call(REESTR_FILE_NAME, shell=True)
# os.startfile(REESTR_FILE_NAME)
