from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
from pprint import pprint
from hashlib import sha256
import requests


def mongo_insert(vacancy_list):
    for el in vacancy_list:
        hash_id = sha256(format(el).encode("utf-8")).hexdigest()
        try:
            collection.insert_one({'_id': hash_id} | el)
        except:
            continue


def hh_parse(vac):
    url = 'https://spb.hh.ru'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    params = {'area': '2', 'fromSearchLine': 'true', 'st': 'searchVacancy'}
    vacancy_info = {'text': vac}
    page_count = int(input('Колличество обрабатываемых страниц: '))
    vacancy_list = []

    for numb in range(page_count):
        page = {'page': numb}
        response = requests.get(url + '/search/vacancy/', params=(params | vacancy_info | page), headers=headers)
        soup = bs(response.text, 'html.parser')
        vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})

        for vacancy in vacancies:
            vacancy_data = {}
            info = vacancy.find('a', {'class': 'bloko-link'})
            name = info.text
            link = info.get('href')

            try:
                price = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
            except:
                price = None

            min_price = None
            max_price = None
            currency = None

            if price:
                price = price.replace('\u202f', '')
                price_list = price.split(' ')

                if price_list[0] == 'до':
                    min_price = None
                    max_price = int(price_list[1])
                    currency = price_list[-1]

                elif price_list[0] == 'от':
                    min_price = int(price_list[1])
                    max_price = None
                    currency = price_list[-1]

                else:
                    min_price = int(price_list[0])
                    max_price = int(price_list[2])
                    currency = price_list[-1]

            price = {'min': min_price, 'max': max_price, 'currency': currency}
            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['price'] = price
            vacancy_data['url'] = url
            vacancy_list.append(vacancy_data)
    return vacancy_list


def db_show():
    show_list = []
    price = int(input('Введите минимальную заработную плату: '))
    for item in collection.find({'price.min': {'$gt': price}}):
        show_list.append(item)
    for item in collection.find({'$and': [{'price.min': None}, {'price.max': {'$gt': price}}]}):
        show_list.append(item)
    return show_list


vacancy = input('Название вакансии: ')
client = MongoClient('127.0.0.1', 27017)
db = client['hh_data']
collection = db[vacancy]

mongo_insert(hh_parse(vacancy))

pprint(db_show())
