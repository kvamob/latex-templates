# Выдергивает из TeX - файла с паспортом скважины параметры скважины и формирует строку для вставки
# в XLS-файл с реестром скважин

import re
import subprocess
import os

FILENAME = 'bhpassport.tex'             # Имя TeX - файла с паспортом скважины

# s = '\newcommand{\txtDepth}{12.0}  % Глубина скважины'
pattern1 = re.compile('{(\d*.\d*)}')     # Шаблон 1
pattern2 = re.compile('.*{.*}{(.*)}')   # Шаблон 2


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

res = '0\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
    'Date', Address, Address, Cadaster, lat, lon, 0, Depth, Debit, full_path)

print(res)
copy2clip(res)
print('\n Результат скопирован в буфер обмена ')

