import sys
import requests
from bs4 import BeautifulSoup


def update():
    url = 'https://www.finanz.ru/valyuty/v-realnom-vremeni'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    data_value = soup.find('table', class_='quote_list')
    without_headlines = data_value.find_all('td')

    currencies = ['Рубль', 'Евро', 'Доллар США', 'Японская иена',
                  'Фунт стерлингов', 'Швейцарский франк', 'Украинская гривна']
    headlines = ['Предложение', 'Предыдущее закрытие',
                 '%', 'Абсолютное значение', 'Время']

    res = []
    prom = []
    for line in without_headlines:  # перевод спарсенных данных в список
        i = line.text
        if i.strip():
            if i.strip() != '-':
                prom.append(i.replace(u'\xa0', u' '))
        else:
            res.append(prom)
            prom = []

    res.append(prom)  # последняя строка не добавляется т.к. после неё нет пробела
    del res[0]  # из-за того что data начинается с пустой строки в res первым добавляется пустой список.
    del prom

    with open('url_data_values.txt', 'w',
              encoding='utf-8') as time_file:  # запись списка данных вместе с заголовками в txt файл
        headlines_detect = 0
        j = 7
        val_num = 0
        time_file.writelines(currencies[val_num] + ' ' + ' '.join(headlines) + '\n')
        val_num += 1
        for i in res:
            time_file.writelines(' '.join(i) + '\n')
            j -= 1
            if j <= 4:
                headlines_detect += 1
            if headlines_detect == 4:
                if val_num <= len(currencies) - 1:
                    time_file.writelines(currencies[val_num] + ' ' + ' '.join(headlines) + '\n')
                    headlines_detect = 0
                    val_num += 1
