# make_bhpassport.py
# Создает каталог с паспортом скважины на основе TeX-файла - готового отчета по поискам подземных вод, копирует туда
# необходимые файлы и заполняет шапку паспорта (адрес, кадастровый номер, координаты)
# Каталог создается в папке, задаваемой переменной BHPASSPORTS_PATH
# Данные для заполнения шапки паспорта находятся в TeX файле с отчетом (TEX_REPORT_FILE), лежащем в текущей папке

import shutil
import os
import sys
import webbrowser
from jinja2 import Template


BHPASSPORTS_PATH = 'D:\Home System\ИЗЫСКАНИЯ\Паспорта скважин\2018'  # Путь к папке с отчетами по изысканиям
TEX_REPORT_FILE = 'water.tex'                                        # Имя TeX файла - отчета по изысканиям



def modify_tex_file(filename, address, cadaster, nomenclature, coords):
    """
        Заменим поля адреса участка, кадастрового номера и номенклатуры в шаблонном tex-файле на
        реальные
        Используется шаблонизатор Jinja2
    """

    # Словарь, содержащий ключи - имена переменных в tex шаблоне, которые заменяются на значения,
    # переданные в функцию
    # Например, строка \newcommand{\txtAddress}{{ ADDRESS }} заменяется на
    # \newcommand{\txtAddress}{Свердловская обл., р-н Каменский, СТ Россия}
    data = {
        'ADDRESS': '{' + address + '}',
        'CADASTER': '{' + cadaster + '}',
        'NOMENCLATURE': '{' + nomenclature + '}',
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


def make_ozi_file(filename, content):
    """
    Запишем координаты в файл Ozi Explorer Waypoints
    filename - полный путь к файлу
    """
    try:
        with open(filename, 'w') as out_file:
            out_file.write(content)
            print('>>> Создаем файл Ozi Waypoints ', filename)
    except IOError as e:
        print('*** Ошибка записи в файл {0}: {1} '.format(filename, e), file=sys.stderr)


def gen_report_folder(addr):
    """
    # Сгенерировать имя папки по шаблону: Адрес Месяц Год
    addr - адрес
    Возвращает сгенерированную строку
    """
    locale.setlocale(locale.LC_ALL, "")  # Чтобы дата и время выдавались в текущей локали
    return '{0} {1}'.format(addr.replace('\"', ''), datetime.now().strftime('%B %Y'))


def copy_report_folder(src, dst):
    """
    # Копируем папку с шаблоном отчета в папку с изысканиями
    src - полный путь к папке с шаблонами отчета
    dst - полный путь к папке c отчетами по изысканиям
    """
    retval = ''
    try:
        print('>>> Копируем шаблон отчета в папку: {0}'.format(dst))
        shutil.copytree(src, dst)
        print('>>> Шаблон скопирован.')
    except IOError as e:
        retval = '*** Ошибка копирования: {0}'.format(e)
    return retval

#######################################################################################################################
#
#                                                    M A I N
#
#######################################################################################################################
if __name__ == '__main__':

# Запишем координаты в файл Ozi Explorer Waypoints
    make_ozi_file(settings.OZI_WAYPOINTS_FILE, area.ozi_info)

    locale.setlocale(locale.LC_ALL, "")  # Чтобы дата и время выдавались в текущей локали

    address = area.address
    nomenclature = area.nomenclature
    coords = area.coords

    dst_folder = gen_report_folder(area.address)

    # Копируем папку с шаблоном отчета в папку с изысканиями
    dst_path = os.path.join(settings.REPORTS_PATH, dst_folder)
    # print('>>> Копируем шаблон отчета в папку', dst_path)
    err = copy_report_folder(settings.TEX_TEMPLATE_PATH, dst_path)
    if err:
        print(err, file=sys.stderr)
        exit(-1)
    else:
        print('>>> Шаблон скопирован')

    # Заменим в файле шаблона water.tex адрес, кад. номер и номенклатуру на реальные
    filename = os.path.join(dst_path, settings.TEX_TEMPLATE_FILE)
    modify_tex_file(filename, address, cadaster, nomenclature, coords)

    # Откроем проводник в папке назначения
    webbrowser.open(dst_path)
##################################################################################################################



