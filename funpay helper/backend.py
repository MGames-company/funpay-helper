import time
import os
import pickle
import selenium
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.devtools.v85.page import delete_cookie
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json


options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.3')
options.add_argument('--window-size=1920,1080')
#options.add_argument('--disable-cache')
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10, poll_frequency=1)
login_success = False
def write_text_to_file(text):
    with open('log.txt', 'a') as f:
        f.write(text + "\n")
with open('Cookie.json', 'r') as file:
    data = json.load(file)
goldenkey_value = None
phpsessid_value = None
for cookie in data:
    if cookie["name"] == 'golden_key':
        goldenkey_value = cookie["value"]
    elif cookie["name"] == 'PHPSESSID':
        phpsessid_value = cookie["value"]

# Выводим значения
print("Golden Key Value:", goldenkey_value)
print("PHPSESSID Value:", phpsessid_value)
def login():
    write_text_to_file('Запущен процесс входа в аккаунт')
    #print('Запущен процесс входа в аккаунт')

    passwordvk = '7Matilda13'
    mailvk = 'Timon-2007@bk.ru'
    driver.get('https://funpay.com/')
    loggin = ('xpath', '//a[@class = \'menu-item-login\']')
    driver.find_element(*loggin).click()
    time.sleep(1)
    VK = ('xpath','//a[@class = \'social-login-item social-login-item-vk\']')
    driver.find_element(*VK).click()
    wait.until(EC.presence_of_element_located(("xpath" , "//label[2]"))).click()
    mail = ('xpath', '//input[@type = \'text\']')
    driver.find_element(*mail).send_keys(mailvk)
    time.sleep(3)
    driver.find_element('xpath', '//button[@type = \'submit\']').click()
    wait.until(EC.presence_of_element_located(("xpath" , "//input[@name = \'password\']"))).send_keys(passwordvk)
    time.sleep(3)
    driver.find_element('xpath', '//button[@type = \'submit\']').click()
    time.sleep(7)
    #driver.delete_cookie('golden_key')
    #driver.delete_cookie('PHPSESSID')
    #driver.add_cookie({'name': 'golden_key', 'value': goldenkey_value })
    #driver.add_cookie({'name': 'PHPSESSID', 'value': phpsessid_value })
    driver.refresh()
    driver.find_element('xpath','//a[@class =\"dropdown-toggle user-link\"]').click()
    wait.until(EC.presence_of_element_located(('xpath','//ul[@class = \'dropdown-menu\']//a[@class=\'user-link-dropdown\']'))).click()
    write_text_to_file('Успешный вход')
stop = False
a = list()
def up_offers():
    wait.until(EC.presence_of_element_located(('xpath', '//a[@class="btn btn-default btn-plus"]')))
    offers = driver.find_elements('xpath', '//a[@class="btn btn-default btn-plus"]')
    count_offers = len(offers)
    for count_offers in range(count_offers): #Поднятие лотов
        if stop == True:
            return
        xpath = 'xpath'
        el = '(//a[@class="btn btn-default btn-plus"])'
        el2 = '['
        k = count_offers + 1
        el3 = str(k)
        el4 = ']'
        el5 = el + el2 + el3 + el4
        cort = ()
        cort += (xpath,el5)
        print(*cort)
        wait.until(EC.presence_of_element_located(('xpath', '//a[@class="btn btn-default btn-plus"]'))) #ждём отображения кнопки редактирования лотов
        driver.find_element(*cort).click()
        wait.until(EC.presence_of_element_located(('xpath', '//button[@class="btn btn-default btn-block js-lot-raise"]'))).click() #поднимаем предложения
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        try:
            Current_url = driver.current_url
            time_slots = wait.until(EC.presence_of_element_located(('xpath','//div[@class="ajax-alert ajax-alert-danger"]')))
            a.append(time_slots.text)
            #cul = '[АВТОПОДНЯТИЕ] не удалось поднять лоты: ' + Current_url
            #write_text_to_file(cul)

        except:
            Current_url1 = driver.current_url
            cul1 ='[АВТОПОДНЯТИЕ] Поднял лоты: ' + Current_url1
            print('не найден текст')
            write_text_to_file(cul1)
        driver.back()
    print('list:', a)