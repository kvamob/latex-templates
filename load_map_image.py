# Получение карты Yandex Maps по координатам центра
# Описание API https://tech.yandex.ru/maps/doc/staticapi/1.x/dg/concepts/input_params-docpage/
# Результат - в файле ./images/map.png
# Используется библиотека requests (pip3 install requests)


import shutil
import requests

out_filename = './images/map.png'
coords = '43.269124 6.640285'

(lat, lon) = coords.replace(',', '.').split()
scale = 14          # Масштабирование

# url = 'https://static-maps.yandex.ru/1.x/?pt={0},{1},comma&z={2}&size=600,450&l=map,skl'.format(lon, lat, scale)
url = 'https://static-maps.yandex.ru/1.x/?pt={0},{1},comma&z={2}&size=600,450&l=map'.format(lon, lat, scale)

response = requests.get(url, stream=True)
if response.status_code == 200:
    print('Запрос выполнен успешно')
    with open(out_filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
else:
    print('Ошибка, status code: {}'.format(response.status_code))
del response
