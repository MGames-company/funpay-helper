import time
import os
import pickle
from typing import final

import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.devtools.v85.page import delete_cookie
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import json
import sqlite3
import requests

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'
database = 'D:/programs/development/rofls/.venv/funpay helper/data/database.db'
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument("user-data-dir=C:\\Users\\Timon\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.3')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-cache')
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10, poll_frequency=1)
login_success = False
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn
def lastAutoReplyText():
    conn = create_connection(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM autort")
    text = cursor.fetchone()
    text2 = ''.join(map(str, text))
    print(text2)
    return text2
    conn.commit()
    conn.close()
def split_text(input_text):
    parts1 = input_text.replace('%НИК%', author)
    print(author)
    print(parts1)
    parts = parts1.split('\n')
    return parts
def xpath_filter(text):
    xpath1 = 'xpath'
    final = ()
    final += (xpath1, text)
    return final
def write_text_to_file(text):
    with open('D:/programs/development/rofls/.venv/funpay helper/data/log.txt', 'a') as f:
        f.write(text + "\n")
def read_command_from_text():
    with open('D:/programs/development/rofls/.venv/funpay helper/data/Commands.json', 'r') as f:
        commands_text = json.load(f)
        return commands_text
"""
def huita():
    try:
        with open('D:/programs/development/rofls/.venv/funpay helper/data/Cookie.json', 'r') as file:
            data = json.load(file)
    except:
        with open('D:/programs/development/rofls/.venv/funpay helper/data/Cookie.json', 'a') as file:
            file.truncate(0)
            file.write('{}')
        with open('D:/programs/development/rofls/.venv/funpay helper/data/Cookie.json', 'r') as file:
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
"""
def login():
    global Nickname
    write_text_to_file('Запущен процесс входа в аккаунт')
    driver.get('https://funpay.com/')
    driver.find_element('xpath', '//a[@class =\"dropdown-toggle user-link\"]').click()
    wait.until(EC.presence_of_element_located(('xpath', '//ul[@class = \'dropdown-menu\']//a[@class=\'user-link-dropdown\']'))).click()
    nickname = wait.until(EC.presence_of_element_located(('xpath', '//span[@class="mr4"]'))).text
    write_text_to_file(nickname)
    Nickname = str(nickname)
    print(Nickname)
    driver.get('https://funpay.com/orders/trade')
    try:
        while True:
            driver.find_element('xpath','//button[@class="btn btn-default dyn-table-continue"]').click()
    except:
        sells = driver.find_elements('xpath','//a[@class="tc-item"]')
        sells_refund = driver.find_elements('xpath','//a[@class="tc-item warning"]')
        sell_open = driver.find_elements('xpath','//a[@class="tc-item info"]')
        write_text_to_file(str(len(sells_refund)))
        write_text_to_file(str(len(sell_open)))
        sells_all = len(sells)
        write_text_to_file(str(sells_all))
    #//span[@class="mr4"]
    """
    loggin = ('xpath', '//a[@class = \'menu-item-login\']')
    driver.find_element(*loggin).click()
    #'''
    passwordl = '7Vfnbkmlf13'
    maill = 'norismaxi12@gmail.com'
    
    
    time.sleep(1)
    mail = ('xpath', '//input[@name="login"]')
    driver.find_element(*mail).send_keys(maill)
    password = ('xpath','//input[@name="password"]')
    driver.find_element(*password).send_keys(passwordl)
    time.sleep(1)
    #driver.find_element('xpath','//div[@class="recaptcha-checkbox-border"]').click()
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located(('xpath', '//span[@aria-checked="true"]')))
    except:
        print('капча не пройдена')
    #//div[@style = "display: none; animation-play-state: running; opacity: 1;"]
    driver.find_element('xpath','//button[@class="btn btn-primary btn-block"]').click()
    time.sleep(10)
    """
    '''
    mailvk = 'Timon-2007@bk.ru'
    passwordvk = '7Matilda13'
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
    
    driver.delete_cookie('golden_key')
    driver.delete_cookie('PHPSESSID')
    driver.add_cookie({'name': 'golden_key', 'value': goldenkey_value })
    driver.add_cookie({'name': 'PHPSESSID', 'value': phpsessid_value })
    driver.refresh()
    '''
    write_text_to_file('вошел в аккаунт')
Nickname = ''
thread_active = 0
stop = False
a = list()
chat_stop = False
AutoreplyText = lastAutoReplyText()
xpath = 'xpath'
AutoGuard = False
SendNotifications = False
SendMessages = False


def up_offers():
    driver.find_element('xpath','//a[@class =\"dropdown-toggle user-link\"]').click()
    wait.until(EC.presence_of_element_located(('xpath','//ul[@class = \'dropdown-menu\']//a[@class=\'user-link-dropdown\']'))).click()

    try:
        wait.until(EC.presence_of_element_located(('xpath', '//a[@class="btn btn-default btn-plus"]')))
        offers = driver.find_elements('xpath', '//a[@class="btn btn-default btn-plus"]')
        count_offers = len(offers)
        for count_offers in range(count_offers): #Поднятие лотов
            if stop == True:
                return
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
                try:
                    wait.until(EC.presence_of_element_located(('xpath', '//div[@class="checkbox"]')))
                    driver.find_element('xpath','//button[@class="btn btn-primary btn-block js-lot-raise-ex"]').click()


                    #//div[@class="checkbox"]
                    #//button[@class="btn btn-primary btn-block js-lot-raise-ex"]
                    Current_url1 = driver.current_url
                    cul1 ='[АВТОПОДНЯТИЕ] Поднял лоты: ' + Current_url1
                    print('не найден текст')
                    write_text_to_file(cul1)
                except:
                    print('не удалось поднять лоты')
                driver.back()
        print('list:', a)
    except:
        write_text_to_file('Лоты не найдены')
def auto_reply():
    db = sqlite3.connect('D:/programs/development/rofls/.venv/funpay helper/data/database.db')
    c = db.cursor()
    c.execute("SELECT login FROM Steam_Guard")
    logins = c.fetchall()
    if chat_stop == True:
        thread_active = 0
        db.commit()
        db.close()
        return
    try:
        thread_active = 2
        wait.until(EC.presence_of_element_located(('xpath', '//span[@class="badge badge-chat"]')))
        global author
        driver.get('https://funpay.com/chat/')
        #while chat_stop == False:
        if chat_stop == True:
            thread_active = 0
            db.commit()
            db.close()
            return
        try:
            chat = wait.until(EC.element_to_be_clickable(('xpath', '//a[@class ="contact-item unread"]')))
            #//div[contains(text(), 'login: Warfacetop174 password: 7Ujavfy8')]
            chat.click()
            last_message = driver.find_element('xpath', '(//div[@class="chat-msg-text"])[last()]').text
            msg_author = '(//div[@class="chat-msg-item chat-msg-with-head"])[last()]//child::a[@class="chat-msg-author-link"]'
            msg_author_sort = xpath_filter(msg_author)
            Commands = read_command_from_text()
            author = driver.find_element(*msg_author_sort).text
            #//div[@class="chat-msg-text"][contains(text(), 'Warfacetop174')]
            if last_message in Commands:
                command1 = Commands[last_message]
                driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(command1)
                # time.sleep(1)
                driver.find_element('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
                if last_message == '!продавец' and SendNotifications == True:
                    current_url = driver.current_url
                    text = f'👤Покупатель: {author} \n 🔗Ссылка на чат: {current_url}'
                    send_message_to_tgbot(text)
            elif last_message == '!продавец' and SendNotifications == True:
                current_url = driver.current_url
                text = f'👤Покупатель: {author} \n 🔗Ссылка на чат: {current_url}'
                send_message_to_tgbot(text)
            elif last_message == 'Код' and AutoGuard == True:
                for login in logins:
                    try:
                        print(login[0])
                        driver.find_element('xpath',f'//div[@class="chat-msg-text"][contains(text(), "{login[0]}")]')
                        auto_send_guard(login[0])

                        write_text_to_file(f'Выдан код Steam Guard для покупателя {author.text}')
                    except:
                        print('ненаход')

            else:
                #global AutoreplyText = f'Привет, {name}! /nПродавец ответит тебе в ближайшее время./n[funpay Assistant]'
                AutoreplyText = lastAutoReplyText()
                text_send = split_text(AutoreplyText)
                try:
                    for string in text_send:
                        driver.find_element('xpath',f'//div[text() = "{string}"]')
                        print(string)

                    write_text_to_file('такой ответ был')
                except:
                    write_text_to_file('в чате не было такого ответа')
                    for string in text_send:
                        # print(string)
                        driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(string)
                        # time.sleep(1)
                        driver.find_element('xpath',
                                            '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
                        driver.refresh()
            if SendMessages == True and SendNotifications == True:
                current_url = driver.current_url
                notification = f'[Новое сообщение]\nПользователь: {author} \nСообщение:{last_message} \nСсылка на чат: {current_url}'
                send_message_to_tgbot(notification)


            driver.get('https://funpay.com/chat/')

        except :
            time.sleep(5)
            driver.refresh()

        #//a[@class ="contact-item unread"]
    except:
        time.sleep(5)
        driver.refresh()

    finally:
        thread_active = 0
        db.commit()
        db.close()
def auto_send_guard(login):
    windows = driver.window_handles
    if len(windows) < 2:
        driver.execute_script("window.open('https://e.mail.ru/inbox', '_blank');")
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        time.sleep(2)
    else:
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        driver.get('https://e.mail.ru/inbox')

    db = sqlite3.connect('D:/programs/development/rofls/.venv/funpay helper/data/database.db')
    c = db.cursor()
    c.execute(f"SELECT mail FROM Steam_Guard WHERE login = '{login}'")
    mail = c.fetchone()
    time.sleep(3)
    try:
        driver.find_element('xpath',f'//img[@alt="{mail}"]')
    except:
        driver.find_element('xpath','//div[@class="ph-project__user-icon svelte-ttryjx"]').click()
        wait.until(EC.presence_of_element_located(('xpath','//div[text() = "timon-207@bk.ru"]'))).click()
    time.sleep(5)
    s = driver.find_element('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')
    if s:
        s.click()
    else:
        print('не найден элемент')
    guard = wait.until(EC.presence_of_element_located(('xpath', '(//td[@class="title-48_mr_css_attr c-blue1_mr_css_attr fw-b_mr_css_attr a-center_mr_css_attr"])[1]'))).text
    driver.switch_to.window(windows[0])
    #return guard
    driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(guard)
    driver.find_element('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
    db.close()
def send_message_to_tgbot(message):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT Token FROM TGbot")
    Token = cursor.fetchone()
    cursor.execute("SELECT ID FROM TGbot")
    chatid = cursor.fetchone()
    url = f'https://api.telegram.org/bot{Token[0]}/sendMessage'
    payload = {
        'chat_id': chatid[0],
        'text': message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print('Сообщение отправлено!')
    else:
        print('Ошибка при отправке сообщения.')
    conn.close()
