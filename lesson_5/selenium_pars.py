import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from hashlib import sha256


def mongo_insert(product_list):
    for el in product_list:
        hash_id = sha256(format(el).encode("utf-8")).hexdigest()
        try:
            collection.insert_one({'_id': hash_id} | el)
        except:
            continue


driver = webdriver.Firefox(executable_path='./geckodriver.exe')

driver.get('https://www.mvideo.ru/')
driver.maximize_window()

driver.implicitly_wait(10)

elem = driver.find_element_by_tag_name("html")

elem.send_keys(Keys.END)

new_products = driver.find_element_by_xpath(
    '//div[@class="gallery-title-wrapper"]/h2[contains(text(), "Новинки")]/../../..//ul')
time.sleep(4)
driver.execute_script("arguments[0].scrollIntoView();", new_products)

next_button = new_products.find_element_by_xpath('./../..//a[contains(@class, "next-btn")]')

while 'disabled' not in next_button.get_attribute('class'):
    time.sleep(3)
    next_button.click()

mvideo_new_products = new_products.find_elements_by_xpath('./li[contains(@class, "gallery-list-item")]')

mvideo_list = []
for el in mvideo_new_products:
    mvideo_dict = {}

    url = el.find_element_by_tag_name('a').get_attribute('href')

    info = json.loads(el.find_element_by_tag_name('a').get_attribute('data-product-info'))

    title = info['productName']
    price = float(info['productPriceLocal'])

    mvideo_dict['url'] = url
    mvideo_dict['title'] = title
    mvideo_dict['price'] = price

    mvideo_list.append(mvideo_dict)

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_new']
collection = db.mvideo
mongo_insert(mvideo_list)

