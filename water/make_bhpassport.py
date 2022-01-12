# make_bhpassport.py
# Создает каталог с паспортом скважины на основе TeX-файла - готового отчета по поискам подземных вод, копирует туда
# необходимые файлы и заполняет шапку паспорта (адрес, кадастровый номер, координаты)
# Каталог создается в папке, задаваемой переменной BHPASSPORTS_PATH
# Данные для заполнения шапки паспорта находятся в TeX файле с отчетом (TEX_REPORT_FILE), лежащем в текущей папке

import shutil
import os
import sys
import webbrowser
import locale
import codecs
import re
from collections import namedtuple
from jinja2 import Template


BHPASSPORTS_PATH = 'D:\\Home System\\ИЗЫСКАНИЯ\\Паспорта скважин\\2022'  # Путь к корневой папке с паспортами скважин
BHTEMPLATES_PATH = 'D:\\GIT-REPOS\\latex-templates\\bhpassport'          # Путь к папке с шаблонами паспортов скважин
TEX_TEMPLATE_FILE = 'bhpassport.tex'                                     # Имя файла с шаблоном паспорта скважины
TEX_REPORT_FILE = 'water.tex'                                        # Имя TeX файла - отчета по изысканиям
# TEX_REPORT_FILE = 'water_test.tex'                                       # Имя TeX файла - отчета по изысканиям
MAP_FILE = 'map.png'                                                     # Файл с обзорной картой
# MAP_FILE = 'map_test.png'                                                     # Файл с обзорной картой


def modify_tex_file(filename, address, cadaster, coords):
    """
        Заменим поля адреса участка, кадастрового номера и координат в шаблонном tex-файле на реальные
        Используется шаблонизатор Jinja2
    """

    # Словарь, содержащий ключи - имена переменных в tex шаблоне, которые заменяются на значения,
    # переданные в функцию
    # Например, строка \newcommand{\txtAddress}{{ ADDRESS }} заменяется на
    # \newcommand{\txtAddress}{Свердловская обл., р-н Каменский, СТ Россия}
    data = {
        'ADDRESS': '{' + address + '}',
        'CADASTER': '{' + cadaster + '}',
        'COORDINATES': '{' + coords + '}',
    }

    #  Прочитаем файл целиком
    try:
        with codecs.open(filename, 'r', 'utf-8') as input_file:
            template = Template(input_file.read())
        tex = template.render(**data)
    except IOError as e:
        print('*** Ошибка чтения файла', e, file=sys.stderr)
        return

    # А теперь запишем все в тот же файл :
    try:
        with codecs.open(filename, 'w', 'utf-8') as out_file:
            out_file.write(tex)
    except IOError as e:
        print('*** Ошибка записи файла', e, file=sys.stderr)

    return


def gen_bhpassport_folder():
    """
    # Сгенерировать имя выходной папки по шаблону: <Путь к папке с паспортами>\Паспорт <Имя папки с отчетом по воде>
    Возвращает сгенерированную строку
    """
    curr_folder = os.path.basename(os.getcwd())
    dst_folder = 'Паспорт ' + curr_folder
    dst_path = os.path.join(BHPASSPORTS_PATH, dst_folder)
    return dst_path


def copy_bhpassport_folder(src, dst):
    """
    # Копируем папку с шаблоном паспорта скважины в папку с изысканиями
    src - полный путь к папке с шаблонами паспортов
    dst - полный путь к папке паспортами скважин
    """
    retval = ''
    try:
        print('>>> Копируем шаблон паспорта в папку: {0}'.format(dst))
        shutil.copytree(src, dst)
        print('>>> Шаблон скопирован.')
    except IOError as e:
        retval = '*** Ошибка копирования: {0}'.format(e)
    return retval


def copy_map_file(src, dst):
    """
    # Копируем файл карты из отчета в паспорт скважины
    src - полный путь к файлу с картой в папке c отчетом
    dst - полный путь к файлу в папке паспортами скважин
    """
    retval = ''
    try:
        print('>>> Копируем обзорную карту в папку: {0}'.format(dst))
        shutil.copyfile(src, dst)
        print('>>> Файл с картой скопирован.')
    except IOError as e:
        retval = '*** Ошибка копирования: {0}'.format(e)
    return retval


def parse_report(filename):
    """
    Считывает поля из файла filename. Это Tex-файл с отчетом по изысканиям
    Возвращает именованный кортеж, содержащий считанные параметры
    :param filename:
    :return:
    """
    Result = namedtuple('Result', 'errmsg address coords cadaster')
    Result.errmsg = ''

    pattern1 = re.compile('{(\d*.\d*)}')  # Шаблон 1
    pattern2 = re.compile('.*{.*}{(.*)}')  # Шаблон 2

    with open(filename, encoding='utf-8') as file:
        content = file.readlines()

    for line in content:
        # Coordinates
        if re.search(r'.*\\newcommand{\\txtCoords}', line):
            # print(line.strip())
            Result.coords = pattern2.findall(line)[0]
        # Сadaster
        if re.search(r'.*\\newcommand{\\txtCadaster}', line):
            # print(line.strip())
            Result.cadaster = pattern2.findall(line)[0]
        # Address
        if re.search(r'.*\\newcommand{\\txtAddress}', line):
            # print(line.strip())
            Result.address = pattern2.findall(line)[0]

    return Result


#######################################################################################################################
#
#                                                    M A I N
#
#######################################################################################################################


if __name__ == '__main__':

    locale.setlocale(locale.LC_ALL, "")  # Чтобы дата и время выдавались в текущей локали

    area = parse_report(TEX_REPORT_FILE)  # получим именованный кортеж area

    address = area.address
    cadaster = area.cadaster
    coords = area.coords

    # Копируем папку с шаблоном паспорта скважины в папку с изысканиями
    dst_path = gen_bhpassport_folder()
    # dst_path = os.path.join(BHPASSPORTS_PATH, dst_folder)
    # print('>>> Копируем шаблон паспорта скважины в папку', dst_path)
    err = copy_bhpassport_folder(BHTEMPLATES_PATH, dst_path)
    if err:
        print(err, file=sys.stderr)
        exit(-1)
    # else:
    #     print('>>> Шаблон скопирован')

    # Заменим в файле шаблона bhpassport.tex адрес, кад. номер и номенклатуру на реальные
    filename = os.path.join(dst_path, TEX_TEMPLATE_FILE)
    modify_tex_file(filename, address, cadaster, coords)

    # Копируем обзорную карту из папки с отчетом в папку с паспортом скважины
    src_map_path = os.path.join(os.path.curdir, 'images', MAP_FILE)
    dst_map_path = os.path.join(dst_path, 'images', MAP_FILE)
    copy_map_file(src_map_path, dst_map_path)

    # Откроем проводник в папке назначения
    webbrowser.open(dst_path)
##################################################################################################################



