import signal
import sys
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
from selenium.webdriver.common.by import By
import re

database = '../funpay helper/data/database.db'
connection = sqlite3.connect(database)
cursor = connection.cursor()
cursor.execute(f"SELECT UserData FROM UserProfile")
userdata = cursor.fetchone()
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument(f"user-data-dir={userdata[0]}")
cursor.execute(f"SELECT ProfileDirectory FROM UserProfile")
userDir = cursor.fetchone()
options.add_argument(f'--profile-directory={userDir[0]}')
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.3')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-cache')
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10, poll_frequency=1)
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'
connection.commit()
connection.close()

login_success = False
Nickname = ''
thread_active = 0
stop = False
a = list()
chat_stop = False

xpath = 'xpath'
AutoGuard = False
SendNotifications = False
SendMessages = False
offers = []
IsRemindRewiew = False
IsAutoRewiew = False
RentedAccounts = {}

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn
def lastAutoReplyText():
    conn = create_connection(database)
    curs = conn.cursor()
    curs.execute("SELECT * FROM autort")
    text = curs.fetchone()
    text2 = ''.join(map(str, text))
    conn.close()
    return text2
def Cheque():
    conn = create_connection(database)
    curs = conn.cursor()
    curs.execute("SELECT * FROM OrderCheque")
    text = curs.fetchone()
    text2 = ''.join(map(str, text))
    conn.close()
    return text2
def split_text(input_text,nick):
    parts1 = input_text.replace('%НИК%', nick)
    parts = parts1.split('\n')
    return parts
def split_comands(input_text):
    part1 = input_text.replace('\n', '/n')
    parts = part1.split('/n')
    return parts
def xpath_filter(text):
    xpath1 = 'xpath'
    final = ()
    final += (xpath1, text)
    return final
def write_text_to_file(text):
    with open('../funpay helper/data/log.txt', 'a') as f:
        f.write(text + "\n")
def read_command_from_text():
    with open('../funpay helper/data/Commands.json', 'r') as f:
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
    driver.get('https://funpay.com/')
    driver.find_element('xpath', '//a[@class =\"dropdown-toggle user-link\"]').click()
    wait.until(EC.presence_of_element_located(('xpath', '//ul[@class = \'dropdown-menu\']//a[@class=\'user-link-dropdown\']'))).click()
    nickname = wait.until(EC.presence_of_element_located(('xpath', '//span[@class="mr4"]'))).text
    write_text_to_file(f'Текущий аккаунт: {nickname}')
    """
    global hold_balance
    global Balance
    global Nickname
    global sales
    global sales_refund
    global sales_open
    hold_balance = 0
    write_text_to_file('Запущен процесс входа в аккаунт')
    
    driver.find_element('xpath', '//a[@class =\"dropdown-toggle user-link\"]').click()
    wait.until(EC.presence_of_element_located(('xpath', '//ul[@class = \'dropdown-menu\']//a[@class=\'user-link-dropdown\']'))).click()
    
    balance = wait.until(EC.presence_of_element_located(('xpath','//span[@class="badge badge-balance"]'))).text
    Balance = balance
    write_text_to_file(nickname)
    Nickname = str(nickname)
    driver.get('https://funpay.com/orders/trade')
    try:
        while True:
            sales = driver.find_elements('xpath', '//a[@class="tc-item"]')
            sales_refund = driver.find_elements('xpath', '//a[@class="tc-item warning"]')
            sales_open = driver.find_elements('xpath', '//a[@class="tc-item info"]')
            wait.until(EC.presence_of_element_located(('xpath', '//button[@class="btn btn-default dyn-table-continue"]'))).click()

    except:
        write_text_to_file(str(len(sales_refund)))
        write_text_to_file(str(len(sales_open)))
        sells_all = len(sales)
        write_text_to_file(str(sells_all))
    #//span[@class="mr4"]
    """
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
AutoreplyText = lastAutoReplyText()

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
            wait.until(EC.presence_of_element_located(('xpath', '//a[@class="btn btn-default btn-plus"]'))) #ждём отображения кнопки редактирования лотов
            driver.find_element(*cort).click()
            driver.find_element('xpath', '//button[@class="btn btn-default btn-block js-lot-raise"]').click() #поднимаем предложения
            #now = datetime.now()
            #current_time = now.strftime("%H:%M:%S")
            try:
                time_slots = driver.find_element('xpath','//div[@class="ajax-alert ajax-alert-danger"]')
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
                    write_text_to_file(cul1)
                except:
                    Current_url1 = driver.current_url
                    cul1 = '[АВТОПОДНЯТИЕ] Поднял лоты: ' + Current_url1
                    write_text_to_file(cul1)
            driver.back()
            time.sleep(2)
    except:
        write_text_to_file('Лоты не найдены')
def auto_reply():
    db = sqlite3.connect('../funpay helper/data/database.db')
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
        driver.get('https://funpay.com/chat/')
        #while chat_stop == False:
        if chat_stop == True:
            thread_active = 0
            return
        try:
            chat = wait.until(EC.element_to_be_clickable(('xpath', '//a[@class ="contact-item unread"]')))
            chat.click()
            autoreply2()
        except :
            driver.refresh()
        #//a[@class ="contact-item unread"]
    except:
        time.sleep(5)

    finally:
        driver.get('https://funpay.com/chat/')
        thread_active = 0
def autoreply2():
    Commands = read_command_from_text()
    global author
    try:
        db = sqlite3.connect(database)
        c = db.cursor()
        c.execute("SELECT login FROM Steam_Guard")
        logins = c.fetchall()
        last_messag = driver.find_element('xpath', '(//div[@class="chat-msg-text"])[last()]').text
        last_message = last_messag.casefold()
        msg_author = '//div[@class="chat-header"]//div[@class="media-user-name"]'
        msg_author_sort = xpath_filter(msg_author)

        author = driver.find_element(*msg_author_sort).text
        # //div[@class="chat-msg-text"][contains(text(), 'Warfacetop174')]
        current_url = driver.current_url

        try:
            Funpay_message = driver.find_element('xpath', '(//div[@role="alert"])[last()]').text
        except:
            Funpay_message = 'блаблаблаблеблеблеаааблаблаблаблбалба'
        if last_message == Funpay_message and SendNotifications == True:
            notification = f'[Новое уведомление]\nСообщение:{Funpay_message} \nСсылка на чат: {current_url}'
            send_message_to_tgbot(notification)
        else:
            if last_message in Commands:
                command1 = Commands[last_message]
                command1_send = split_comands(command1)
                for string in command1_send:
                    driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(string)
                    driver.find_element('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
                    driver.refresh()
                if last_message == '!продавец' and SendNotifications == True:
                    text = f'👤Покупатель: {author} позвал вас \n 🔗Ссылка на чат: {current_url}'
                    send_message_to_tgbot(text)
            elif last_message == '!продавец' and SendNotifications == True:
                text = f'👤Покупатель: {author} позвал вас \n 🔗Ссылка на чат: {current_url}'
                send_message_to_tgbot(text)
            elif last_message == 'код' and AutoGuard == True:
                try:
                    type, info = Check_lot_type()
                    print(f'Тип:{type}')
                    if type == 'Аренда':
                        info2 = info.split('|')

                        try:
                            mail = info2[len(info2) - 1]
                            IsTimeNotEnd = FindTime(info)
                            if IsTimeNotEnd:
                                auto_send_guard_rent(mail)
                                write_text_to_file(f'Выдан код Steam Guard для покупателя {author}')
                                text = f'Выдан код Steam Guard для покупателя {author} \n 🔗Ссылка на чат: {current_url}'
                                send_message_to_tgbot(text)
                                redaction_lots()
                            else:
                                driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(
                                    'Время аренды вышло.Если вы считаете что произошла ошибка то воспользуйтесь командой Код ещё раз или позовите продавца командой !продавец')
                                wait.until(EC.presence_of_element_located(
                                    ('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
                        except:
                            windows = driver.window_handles
                            driver.switch_to.window(windows[0])
                            driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(
                                'Не удалось выдать код, попробуйте ещё раз ввести команду')
                            wait.until(EC.presence_of_element_located(
                                ('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
                            write_text_to_file(f'Не удалось выдать Steam Guard для покупателя {author.text}')



                    elif type == 'Оффлайн':
                        for login in logins:
                            try:

                                driver.find_element('xpath', f'//div[@class="chat-msg-text"][contains(text(), "{login[0]}")]')
                                auto_send_guard(login[0])
                                write_text_to_file(f'Выдан код Steam Guard для покупателя {author.text}')
                                send_message_to_tgbot(f'Выдан код Steam Guard для покупателя {author.text}')
                            except:
                                windows = driver.window_handles
                                driver.switch_to.window(windows[0])
                                driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(
                                    'Не удалось найти аккаунт. Напишите в чат логин аккаунта и снова используйте команду Код')
                                driver.find_element('xpath',
                                                    '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
                    else:
                        driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(
                            'На этот лот не установлена функция автовыдачи кода, дождитесь продавца')
                        driver.find_element('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
                        if SendNotifications == True:
                            current_url = driver.current_url
                            text = f'👤Покупатель: {author} хочет получить код \n 🔗Ссылка на чат: {current_url}'
                            send_message_to_tgbot(text)
                except:
                    driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(
                        'На этот лот не установлена функция автовыдачи кода, дождитесь продавца')
                    driver.find_element('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
                    if SendNotifications == True:
                        current_url = driver.current_url
                        text = f'👤Покупатель: {author} хочет получить код \n 🔗Ссылка на чат: {current_url}'
                        send_message_to_tgbot(text)
            else:
                # global AutoreplyText = f'Привет, {name}! /nПродавец ответит тебе в ближайшее время./n[funpay Assistant]'
                try:
                    CheckFunpayMessage()
                except:
                    None
        if SendMessages == True and SendNotifications == True:
            current_url = driver.current_url
            try:
                notification = f'[Новое сообщение]\nПользователь: {author} \nСообщение:{last_message} \nСсылка на чат: {current_url}'
            except:
                notification = f'[Новое сообщение]\nПользователь: {author} \nСсылка на чат: {current_url}'
            send_message_to_tgbot(notification)
    except:
        print('ошибка')
    finally:
        db.close()
def send_autoreply_text():
    AutoreplyText = lastAutoReplyText()
    text_send = split_text(AutoreplyText, author)
    try:
        for string in text_send:
            driver.find_element('xpath', f'//div[text() = "{string}"]')

    except:
        write_text_to_file('Ответил покупателю')
        for string1 in text_send:
            wait.until(EC.presence_of_element_located(('xpath', '//textarea[@class="form-control"]'))).send_keys(string1)
            # time.sleep(1)
            wait.until(EC.element_to_be_clickable(
                ('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
            driver.refresh()
def CheckFunpayMessage():
    try:
        messagel1 = driver.find_element('xpath', '(//div[@class="chat-msg-text"])[last()]').text
        print(messagel1)
        messagel2 = driver.find_element('xpath', '(//div[@class="chat-msg-text"])[last() - 1]').text
        print(messagel2)
        try:
            Order = driver.find_element('xpath', '(//a[contains(text(), "заказ ")])[last()]').text
            print(Order)
        except:
            Order = 'pizdaaaaaaaaaaaaahuibomsja'
        try:
            confirm_message = driver.find_element('xpath', '(//a[contains(text(), "заказа")])[last()]').text
            print(confirm_message)
        except:
            confirm_message = 'pizdaaaaaaaaaaaaahuibomsja'
        try:
            if IsAutoRewiew == True:
                autoRewiew()
                return
        except:
            None
        if (confirm_message in messagel1  or confirm_message in messagel2) and IsRemindRewiew == True:
            RemindRewiew()
        elif Order in messagel1 or Order in messagel2:
            send_cheque()
        else:
            send_autoreply_text()
    except:
        print('ошибка')
def autoRewiew():
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute("SELECT Text FROM Review")
    text = c.fetchone()
    driver.find_element('xpath', '(//a[contains(text(), "заказу")])[last()]').click()
    rewiew_message = driver.find_element('xpath', '//textarea[@name="text"]')
    driver.find_element('xpath', '//textarea[@name="text"]').send_keys(f'{text[0]}')
    driver.find_element('xpath', '//button[@data-action="save"]').click()
    db.close()
def send_cheque():
    ChequeText = Cheque()
    cheque_send = split_text(ChequeText, author)
    try:
        for string in cheque_send:
            driver.find_element('xpath', f'//div[text() = "{string}"]')
    except:
        for string1 in cheque_send:
            wait.until(EC.presence_of_element_located(
                ('xpath', '//textarea[@class="form-control"]'))).send_keys(string1)
            wait.until(EC.element_to_be_clickable(
                ('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
            driver.refresh()
def RemindRewiew():
    text_remind = 'Если не затруднит,оставьте пожалуйста отзыв. Буду очень рад)'
    wait.until(EC.presence_of_element_located(
        ('xpath', '//textarea[@class="form-control"]'))).send_keys(text_remind)
    wait.until(EC.element_to_be_clickable(
        ('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
    driver.refresh()
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

    db = sqlite3.connect('../funpay helper/data/database.db')
    c = db.cursor()
    c.execute(f"SELECT mail FROM Steam_Guard WHERE login = '{login}'")
    mail = c.fetchone()
    time.sleep(3)
    try:
        wait.until(EC.presence_of_element_located(('xpath',f'//img[@alt="{mail[0]}"]')))
    except:
        driver.find_element('xpath','//div[@class="ph-project__user-icon svelte-ttryjx"]').click()
        wait.until(EC.presence_of_element_located(('xpath',f'//div[text() = "{mail[0]}"]'))).click()
    time.sleep(3)
    try:
        wait.until(EC.presence_of_element_located(('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')))
        s = driver.find_element('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')
        if s:
            s.click()

        guard = wait.until(EC.presence_of_element_located(('xpath', '(//td[@class="title-48_mr_css_attr c-blue1_mr_css_attr fw-b_mr_css_attr a-center_mr_css_attr"])[1]'))).text

        driver.switch_to.window(windows[0])
        text = f'Код для входа в аккаунт {login}: {guard}'
        #return guard
        wait.until(EC.presence_of_element_located(('xpath', '//textarea[@class="form-control"]'))).send_keys(text)
        driver.find_element('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
        db.close()
    except:
        db.close()
def auto_send_guard_rent(mail):
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

    db = sqlite3.connect('../funpay helper/data/database.db')
    c = db.cursor()
    time.sleep(3)
    try:
        wait.until(EC.presence_of_element_located(('xpath',f'//img[@alt="{mail}"]')))
    except:
        driver.find_element('xpath','//div[@class="ph-project__user-icon svelte-ttryjx"]').click()
        wait.until(EC.presence_of_element_located(('xpath',f'//div[text() = "{mail}"]'))).click()
    time.sleep(3)
    try:

        wait.until(EC.presence_of_element_located(('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')))
        s = driver.find_element('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')
        if s:
            s.click()
        guard = wait.until(EC.presence_of_element_located(('xpath', '(//td[@class="title-48_mr_css_attr c-blue1_mr_css_attr fw-b_mr_css_attr a-center_mr_css_attr"])[1]'))).text
        driver.switch_to.window(windows[0])
        text = f'Код для входа в аккаунт: {guard}'
        driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(text)
        driver.find_element('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
        db.close()
    except:
        print('!!!ошибка!!!')
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
def Check_lot_type():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
        wait.until(EC.presence_of_element_located(('xpath', '(//a[contains(text(), "заказ")])[last()]'))).click()
        account = driver.find_element('xpath', '//span[@class="secret-placeholder"]').text
        print(f'выданный аккаунт: {account}')

        cursor.execute("SELECT login FROM Steam_Guard")
        Logins = cursor.fetchall()
        for login in Logins:
            if login[0] in account:
                type = "Оффлайн"
                info = 'None'
                return type, info

        h = driver.find_element('xpath','//div[@class="param-item"]/h5[text() = "Краткое описание"]/following-sibling::div').text
        cursor.execute("SELECT Lot FROM Rent")
        Lots = cursor.fetchall()
        for Lot in Lots:
            if Lot[0] in h:
                print(f"Это аренда, {Lot[0]}")
                cursor.execute(f"SELECT Info FROM Rent WHERE Lot = ?", (Lot[0],))
                info = cursor.fetchone()
                if info[0]:
                    type = 'Аренда'
                    print(f'Тип: {type}')
                    return type, info[0]
                else:
                    print('На этот лот не установлена функция автовыдачи')
                    type = 'None'
                    info = 'None'
                    return type, info
    except:
        cursor.execute("SELECT login FROM Steam_Guard")
        Logins = cursor.fetchall()
        for login in Logins:
            try:
                account = driver.find_element('xpath',f'//div[@class="chat-msg-text"][contains(text(), "{login[0]}")]')
                type = "Оффлайн"
                info = 'None'
                return type, info
            except:
                None
        wait.until(EC.presence_of_element_located(('xpath', '//textarea[@class="form-control"]'))).send_keys('Вы не приобретали аккаунт у продавца.')
        # time.sleep(1)
        wait.until(
            EC.element_to_be_clickable(('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
    conn.close()
def Parsing_lots():
    offers.clear()
    driver.get('https://funpay.com/users/5783166/')
    try:
        a = driver.find_elements('xpath','//a[@class="tc-item"]')
        for element in a:
            if 'Аренда' in element.text:
                offers.append(element.text)
            else:
                None
    except:




        """
        try:
            b = driver.find_element('xpath','//div[@data-section-type="lot"]')
            print(f'2{b.text}')
        except:
            try:
                c = driver.find_element('xpath','//div[@class="offer-tc-container"]')
                print(f'3{c.text}')
            except:
                try:
                    d = driver.find_element('xpath','//div[@class="tc-desc-text"]')
                    print(f'4{d.text}')
                except:
                    print('это просто пиздец')

"""
def FindTime(info):
    db = sqlite3.connect(database)
    c = db.cursor()
    wait.until(EC.presence_of_element_located(('xpath', '(//a[contains(text(), "заказ")])[last()]'))).click()
    time.sleep(2)
    print(info)
    try:
        c.execute(f"SELECT Time FROM Rent WHERE Info = '{info}'")
        text1 = c.fetchone()
        text = driver.find_element('xpath', '//span[@class="text-nowrap"]')
        match = re.search(r'\d+', text1[0])
        if match:
            number = int(match.group())
            # Умножаем число на 60, если в тексте есть слово "час"
            if 'час' in text1[0]:
                number *= 1
            if 'дн' in text1[0]:
                number *= 24
        else:
            number = 1
            if 'час' in text1[0]:
                number *= 1
            if 'дн' in text1[0] or 'день' in text1[0]:
                number *= 24
        print(number)
        match2 = re.search(r'\d+', text.text)
        if match2:
            number2 = int(match2.group())
            # Умножаем число на 60, если в тексте есть слово "час"
            if 'мин' in text.text:
                number2 = 0
            if 'час' in text.text:
                number2 *= 1
            if 'дн' in text.text:
                number2 *= 24
        else:
            number2 = 1
            if 'мин' in text.text:
                number2 = 0
            if 'час' in text.text:
                number2 *= 1
            if 'дн' in text.text or 'день' in text.text:
                number2 *= 24
        result = number >= number2
        print(number2)
        print(result)
        db.close()
        return result
    except:
        print('ничего')

    db.close()
def redaction_lots():
    db = sqlite3.connect(database)
    c = db.cursor()
    account = driver.find_element('xpath', '//span[@class="secret-placeholder"]').text
    lot_name = driver.find_element('xpath',
                                   '//div[@class="param-item"]/h5[text() = "Краткое описание"]/following-sibling::div').text
    print(account)
    print(lot_name)
    c.execute(f"SELECT Time FROM Rent WHERE Lot == '{lot_name}'")
    Time = c.fetchone()
    c.execute(f"SELECT URL FROM Rent WHERE Lot == '{lot_name}'")
    url = c.fetchone()
    driver.get(url[0])
    lots_count = driver.find_elements('xpath', '//div[@class="tc-desc"]')
    time1 = FilterTime(Time[0])
    if account in RentedAccounts:
        db.close()
        return
    else:
        RentedAccounts[account] = [time1, 0]
        print(RentedAccounts)
        for i in range(len(lots_count)):
            IsCorrectLot = False
            try:
                driver.find_element('xpath', f'(//div[@class="tc-desc"])[{i+2}]').click()
                string_text = wait.until(EC.presence_of_element_located(('xpath','//textarea[@class="form-control textarea-lot-secrets"]'))).get_attribute("value")
                print(string_text)
                z = string_text.split('\n')
                for v in z:
                    if account == v:
                        z.remove(v)
                        IsCorrectLot = True
                print(len(z))
                if len(z) > 0 and IsCorrectLot == True:
                    convertList = '\n'.join(z)
                    driver.find_element('xpath', '//textarea[@class="form-control textarea-lot-secrets"]').clear()
                    driver.find_element('xpath', '//textarea[@class="form-control textarea-lot-secrets"]').send_keys(convertList)
                    driver.find_element('xpath','//button[@type="submit"][text() = "Сохранить"]').click()
                elif len(z) == 0 and IsCorrectLot == True:
                    driver.find_element('xpath', '//textarea[@class="form-control textarea-lot-secrets"]').clear()
                    driver.find_element('xpath','//label[contains(text(),"Активное")]').click()
                    driver.find_element('xpath', '//button[@type="submit"][text() = "Сохранить"]').click()
                else:
                    driver.back()
                time.sleep(1)
            except:
                print('фиаско')
                time.sleep(1)
                driver.get(url[0])
        send_message_to_tgbot(f'Убрал из автовыдачи аккаунт {account}, можно выставлять через {Time[0]}')
        db.close()
def replace_lots(data):
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute("SELECT Info FROM Rent")
    logins = c.fetchall()
    unique_logins = list({login for login in logins})
    print(unique_logins)
    print(len(unique_logins))
    for i in range(len(unique_logins)):
        logins_sort = unique_logins[i][0]
        print(logins_sort)
        login = logins_sort.split('|')
        print(login)
        for log in login:
            if log in data:
                c.execute(f"SELECT URL FROM Rent WHERE Info == '{logins_sort}'")
                url = c.fetchone()
                print(url[0])
                driver.get(url[0])
                wait.until(EC.presence_of_element_located(('xpath', '//div[@class="tc-desc"]')))
                lots_count = driver.find_elements('xpath', '//div[@class="tc-desc"]')
                for i in range(len(lots_count)):
                    IsCorrectLot = False
                    driver.find_element('xpath', f'(//div[@class="tc-desc"])[{i + 2}]').click()
                    string_text = wait.until(EC.presence_of_element_located(('xpath', '//textarea[@class="form-control textarea-lot-secrets"]'))).get_attribute("value")
                    print(string_text)
                    for j in range(len(login)):
                        if login[j] in string_text:
                            IsCorrectLot = True
                            print(IsCorrectLot)
                    list_logins = string_text.split('\n')
                    print(len(string_text))
                    if data in list_logins:
                        driver.back()
                    else:
                        if IsCorrectLot == True and len(string_text) > 0:
                            list_logins.append(f'{data}')
                            convertedList = '\n'.join(list_logins)
                            driver.find_element('xpath', '//textarea[@class="form-control textarea-lot-secrets"]').clear()
                            driver.find_element('xpath', '//textarea[@class="form-control textarea-lot-secrets"]').send_keys(convertedList)
                            time.sleep(1)
                            driver.find_element('xpath', '//button[@type="submit"][text() = "Сохранить"]').click()
                        elif len(string_text) == 0:
                            list_logins.append(f'{data}')
                            convertedList = '\n'.join(list_logins)
                            driver.find_element('xpath','//textarea[@class="form-control textarea-lot-secrets"]').send_keys(convertedList)
                            driver.find_element('xpath', '//label[contains(text(),"Активное")]').click()
                            driver.find_element('xpath', '//button[@type="submit"][text() = "Сохранить"]').click()
                    driver.get(url[0])
                    time.sleep(1)
    db.close()
def FilterTime(text):
    match1 = re.search(r'\d+', text)
    if match1:
        number = int(match1.group())
        # Умножаем число на 60, если в тексте есть слово "час"
        if 'час' in text:
            number *= 1
        if 'дн' in text:
            number *= 24
    else:
        number = 1
        if 'час' in text:
            number *= 1
        if 'дн' in text or 'день' in text:
            number *= 24
    return number