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
options.add_argument('--headless')
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
order_list = []

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn
def LoadBlackList():
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute("SELECT Text FROM BlackList")
    Nicknames = c.fetchone()
    ListNicknames = Nicknames[0].split('\n')
    db.close()
    return ListNicknames
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
    #parts = parts1.split('\n')
    return parts1
def split_cheque(text,nick,price,order):
    textOrder = driver.find_element('xpath', '(//div[@class="alert alert-with-icon alert-info"])[last()]').text
    textOrder1 = textOrder.lower()
    print(textOrder1)
    db= sqlite3.connect(database)
    c = db.cursor()
    c.execute("SELECT Criteria FROM ChequePrefs")
    criteries = c.fetchall()
    c.execute("SELECT text FROM ChequePrefs")
    texts = c.fetchall()
    for i in range(len(criteries)):
        print(criteries[i][0])
        if criteries[i][0] in textOrder1:
            text += f'\n{texts[i][0]}'
            print(text)

    part1 = text.replace('%НИК%', nick)
    order1 = order.split('#')
    part2 = part1.replace('%ЗАКАЗ%',order1[1])
    part3 = part2.replace('%ЦЕНА%',price)
    return part3
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
def login():
    global Balance
    global hold_balance
    global Nickname
    global categories_count
    global offers_count
    hold_balance = 0
    driver.get('https://funpay.com/')
    driver.find_element('xpath', '//a[@class =\"dropdown-toggle user-link\"]').click()
    wait.until(EC.presence_of_element_located(('xpath', '//ul[@class = \'dropdown-menu\']//a[@class=\'user-link-dropdown\']'))).click()
    categories = driver.find_elements('xpath', '//a[@class="btn btn-default btn-plus"]')
    offers = driver.find_elements('xpath','//div[@class="tc-desc-text"]')
    offers_count = len(offers)
    categories_count = len(categories)
    nickname = wait.until(EC.presence_of_element_located(('xpath', '//span[@class="mr4"]'))).text
    write_text_to_file(f'Текущий аккаунт: {nickname}')
    balance = wait.until(EC.presence_of_element_located(('xpath', '//span[@class="badge badge-balance"]'))).text
    Balance = balance
    driver.get('https://funpay.com/orders/trade?id=&buyer=&state=paid&game=')
    summ = driver.find_elements('xpath','//div[@class="tc-price text-nowrap tc-seller-sum"]')
    for i in range(len(summ)):
        price = driver.find_element('xpath',f'(//div[@class="tc-price text-nowrap tc-seller-sum"])[{i+1}]').text
        match = re.search(r'\d+', price)
        number = float(match.group())
        hold_balance += number
    Nickname = nickname

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
            time.sleep(2)
            try:
                time_slots = driver.find_element('xpath','//div[@class="ajax-alert ajax-alert-danger"]')
                print('//div[@class="ajax-alert ajax-alert-danger"]')
                #cul = '[АВТОПОДНЯТИЕ] не удалось поднять лоты: ' + Current_url
                #write_text_to_file(cul)
            except:
                try:
                    driver.find_element('xpath','//div[@class="ajax-alert ajax-alert-info"]')
                    print('//div[@class="ajax-alert ajax-alert-info"]')


                    #//div[@class="checkbox"]
                    #//button[@class="btn btn-primary btn-block js-lot-raise-ex"]
                    Current_url1 = driver.current_url
                    cul1 ='[АВТОПОДНЯТИЕ] Поднял лоты: ' + Current_url1
                    write_text_to_file(cul1)
                except:
                    Current_url1 = driver.current_url
                    print('//div[@class="checkbox"]')
                    wait.until(EC.presence_of_element_located(('xpath', '//div[@class="checkbox"]')))
                    driver.find_element('xpath','//button[@class="btn btn-primary btn-block js-lot-raise-ex"]').click()
                    cul1 = '[АВТОПОДНЯТИЕ] Поднял лоты: ' + Current_url1
                    write_text_to_file(cul1)
            driver.back()
            time.sleep(2)
    except:
        write_text_to_file('Лоты не найдены')


def auto_reply():
    windows = driver.window_handles
    driver.switch_to.window(windows[0])
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
            username = driver.find_element('xpath','//a[@class ="contact-item unread"]//div[@class="media-user-name"]').text
            print('username:',username)
            BlackListNicknames = LoadBlackList()
            print(BlackListNicknames)
            for Nick in BlackListNicknames:
                if Nick == username:
                    if SendNotifications == True:
                        chat.click()
                        current_url = driver.current_url
                        text = f'[УВЕДОМЛЕНИЕ]\n😡Пользователь: {Nick} из вашего чёрного списка прислал сообщение.\n🔗Ссылка на чат: {current_url}'
                        send_message_to_tgbot(text)
                    else:
                        print('pohui')
                        time.sleep(3)
                    return

            chat.click()
            autoreply2()
        except :
            driver.refresh()
        #//a[@class ="contact-item unread"]
    except:
        time.sleep(5)

    finally:
        driver.get('https://funpay.com/chat/')
        db.close()
        thread_active = 0
def autoreply2():
    Commands = read_command_from_text()
    global author
    global current_url
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
                input_element = driver.find_element('xpath', '//textarea[@class="form-control"]')
                driver.execute_script("arguments[0].value = arguments[1];", input_element, command1)
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
                                send_text('Запущен процесс выдачи кода,подождите пожалуйста')
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
                            try:
                                write_text_to_file(f'Не удалось выдать Steam Guard для покупателя {author.text}')
                            except:
                                write_text_to_file('Не удалось выдать Steam Guard для покупателя')



                    elif type == 'Оффлайн':
                        for login in logins:
                            try:
                                send_text('Запущен процесс выдачи кода,подождите пожалуйста')
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
            elif last_message == 'код rockstar' and AutoGuard == True:
                try:
                    type, info = Check_lot_type()
                    print(f'Тип:{type}')
                    if type == 'Аренда':
                        info2 = info.split('|')
                        try:
                            mail = info2[len(info2) - 1]
                            IsTimeNotEnd = FindTime(info)
                            if IsTimeNotEnd:
                                send_text('Запущен процесс выдачи кода,подождите пожалуйста')
                                auto_send_guard_rent(mail)
                                write_text_to_file(f'Выдан код Rockstar для покупателя {author}')
                                text = f'Выдан код Rockstar для покупателя {author} \n 🔗Ссылка на чат: {current_url}'
                                send_message_to_tgbot(text)
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
                            try:
                                write_text_to_file(f'Не удалось выдать код Rockstar для покупателя {author.text}')
                            except:
                                write_text_to_file('Не удалось выдать код Rockstar для покупателя')
                    else:
                        send_text('На этот лот не установлена функция автовыдачи кода, дождитесь продавца')
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
                    print('ошибка 2')
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
        driver.find_element('xpath', f'//div[text() = "{text_send}"]')

    except:
        write_text_to_file('Ответил покупателю')

        input_element = wait.until(EC.presence_of_element_located(('xpath', '//textarea[@class="form-control"]')))
        driver.execute_script("arguments[0].value = arguments[1];", input_element, text_send)
        wait.until(EC.element_to_be_clickable(
            ('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
        driver.refresh()
def CheckFunpayMessage():
    try:
        ChequeText = Cheque()
        messagel1 = driver.find_element('xpath', '(//div[@class="chat-msg-text"])[last()]').text
        print(messagel1)
        messagel2 = driver.find_element('xpath', '(//div[@class="chat-msg-text"])[last() - 1]').text
        print(messagel2)
        try:
            Order = driver.find_element('xpath', '(//a[contains(text(), "заказ ")])[last()]').text
            driver.find_element('xpath', '(//a[contains(text(), "заказ ")])[last()]').click()
            price = wait.until(EC.presence_of_element_located(('xpath','//span[@class="h1 mr4 text-bold"]'))).text
            print(Order)
        except:
            Order = 'None'
        try:
            confirm_message = driver.find_element('xpath', '(//a[contains(text(), "заказа")])[last()]').text
            print(confirm_message)
        except:
            confirm_message = 'None'
        try:
            if IsAutoRewiew == True:
                autoRewiew()
                return
        except:
            None
        try:
            rewiew = driver.find_element('xpath', '(//a[contains(text(), "заказу")])[last()]').text
            print(rewiew)
        except:
            rewiew = 'none'
        if (confirm_message in messagel1  or confirm_message in messagel2) and IsRemindRewiew == True:
            RemindRewiew()
        elif Order in messagel1 or Order in messagel2:
            send_cheque(price,Order)
        elif rewiew in messagel1:
            None
        elif ChequeText in messagel1:
            None
        else:
            send_autoreply_text()
    except:
        send_autoreply_text()
def autoRewiew():
    db = sqlite3.connect(database)
    c = db.cursor()
    c.execute("SELECT Text FROM Review")
    text = c.fetchone()
    driver.find_element('xpath', '(//a[contains(text(), "заказу")])[last()]').click()
    input_element = driver.find_element('xpath', '//textarea[@name="text"]')
    driver.execute_script("arguments[0].value = arguments[1];", input_element, text[0])
    driver.find_element('xpath', '//button[@data-action="save"]').click()
    db.close()
def send_cheque(price,order):
    ChequeText = Cheque()
    cheque_send = split_cheque(ChequeText, author,price,order)
    try:
        driver.find_element('xpath', f'//div[text() = "{cheque_send}"]')
    except:
        input_element = wait.until(EC.presence_of_element_located(('xpath', '//textarea[@class="form-control"]')))
        driver.execute_script("arguments[0].value = arguments[1];", input_element, cheque_send)
        wait.until(EC.element_to_be_clickable(
            ('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
        send_message_to_tgbot(f'[ПРОДАЖА]\n👤Покупатель:{author}\n💲Сумма: {price}₽\n🔗Ссылка на чат: {current_url}')
        type, info = Check_lot_type()
        if type == 'Аренда':
            redaction_lots()
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
        driver.switch_to.window(windows[0])
    db.close()
def auto_send_rockstar_code(mail):
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

        wait.until(EC.presence_of_element_located(('xpath','(//span[text() = "Ваш проверочный код Rockstar Games"] | //span[text() = "Your Rockstar Games verification code"])')))
        s = driver.find_element('xpath','(//span[text() = "Ваш проверочный код Rockstar Games"] | //span[text() = "Your Rockstar Games verification code"])')
        if s:
            s.click()
        guard = wait.until(EC.presence_of_element_located(('xpath', '//span[@class="rc-2fa-code_mr_css_attr rc-2fa-code-override_mr_css_attr"]'))).text
        driver.switch_to.window(windows[0])
        text = f'Код для входа в аккаунт rockstar: {guard}'
        driver.find_element('xpath', '//textarea[@class="form-control"]').send_keys(text)
        driver.find_element('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']').click()
        db.close()
    except:
        print('!!!ошибка!!!')
        driver.switch_to.window(windows[0])
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


        cursor.execute("SELECT login FROM Steam_Guard")
        Logins = cursor.fetchall()
        for login in Logins:
            if login[0] in account:
                type = "Оффлайн"
                info = 'None'
                return type, info

        h = driver.find_element('xpath','//div[@class="param-item"]/h5[text() = "Краткое описание"]/following-sibling::div').text
        print(h)
        cursor.execute("SELECT Lot FROM Rent")
        Lots = cursor.fetchall()
        print(Lots)
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
        None
def FindTime(info):
    db = sqlite3.connect(database)
    c = db.cursor()
    wait.until(EC.presence_of_element_located(('xpath', '(//a[contains(text(), "заказ")])[last()]'))).click()
    time.sleep(2)
    print(info)
    try:
        c.execute(f"SELECT Time FROM Rent WHERE Info = '{info}'")
        text1 = c.fetchone()
        text = driver.find_element('xpath', '//span[@class="text-nowrap"]').text
        match = re.search(r'\d+', text1[0])
        if match:
            number = int(match.group())
            # Умножаем число на 60, если в тексте есть слово "час"
            if 'час' in text1[0]:
                number *= 1
            elif 'дн' in text1[0]:
                number *= 24
            else:
                number *= 0
        else:
            number = 1
            if 'час' in text1[0]:
                number *= 1
            elif 'дн' in text1[0] or 'день' in text1[0]:
                number *= 24
            else:
                number *= 0
        print(number)
        match2 = re.search(r'\d+', text)
        if match2:
            number2 = int(match2.group())
            if 'мин' in text:
                number2 = 0
            elif 'час' in text:
                number2 *= 1
            elif 'дн' in text:
                number2 *= 24
            elif 'сек' in text:
                number2 = 0
        else:
            number2 = 1
            if 'мин' in text:
                number2 = 0
            elif 'час' in text:
                number2 *= 1
            elif 'дн' in text or 'день' in text:
                number2 *= 24
            elif 'сек' in text:
                number2 = 0
        if number2 > 24:
            number2 = 0
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
    accounts = driver.find_elements('xpath', '//span[@class="secret-placeholder"]')
    list_accounts = []
    for i in range(len(accounts)):
        account = wait.until(EC.presence_of_element_located(('xpath', f'(//span[@class="secret-placeholder"])[{i+1}]'))).text
        list_accounts.append(account)
    print(list_accounts)
    lot_name = wait.until(EC.presence_of_element_located(('xpath','//div[@class="param-item"]/h5[text() = "Краткое описание"]/following-sibling::div'))).text
    print(lot_name)
    c.execute(f"SELECT Time FROM Rent WHERE Lot == '{lot_name}'")
    Time = c.fetchone()
    print(Time[0])
    c.execute(f"SELECT URL FROM Rent WHERE Lot == '{lot_name}'")
    url = c.fetchone()
    print(url[0])
    driver.get(url[0])
    wait.until(EC.presence_of_element_located(('xpath', '//div[@class="tc-desc"]')))
    lots_count = driver.find_elements('xpath', '//div[@class="tc-desc"]')
    time1 = FilterTime(Time[0])
    for account in list_accounts:
        if account in RentedAccounts:
            db.close()
        else:
            RentedAccounts[account] = [time1, 0]
            print(RentedAccounts)
            for i in range(len(lots_count)):
                IsCorrectLot = False
                try:
                    driver.find_element('xpath', f'(//div[@class="tc-desc"])[{i+2}]').click()
                    string_text = wait.until(EC.presence_of_element_located(('xpath','//textarea[@class="form-control textarea-lot-secrets"]'))).get_attribute("value")
                    z = string_text.split('\n')
                    for v in z:
                        if account == v:
                            z.remove(v)
                            IsCorrectLot = True
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
    for i in range(len(unique_logins)):
        logins_sort = unique_logins[i][0]
        print(logins_sort)
        login = logins_sort.split('|')
        print(login)
        for log in login:
            if log in data:
                c.execute(f"SELECT URL FROM Rent WHERE Info == '{logins_sort}'")
                url = c.fetchone()
                driver.get(url[0])
                wait.until(EC.presence_of_element_located(('xpath', '//div[@class="tc-desc"]')))
                lots_count = driver.find_elements('xpath', '//div[@class="tc-desc"]')
                for i in range(len(lots_count)-1):
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
                        #elif IsCorrectLot == False and len(string_text) > 0:
                            #print('не тот лот')
                    driver.get(url[0])
                    time.sleep(1)
                try:
                    driver.find_element('xpath', '//a[@class="tc-item warning"]').click()
                    wait.until(EC.presence_of_element_located(('xpath', '//label[contains(text(),"Активное")]'))).click()
                except:
                    None

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
def CloseApp():
    driver.close()
    sqlite3.connect(database).close()
def IfError():
    windows = driver.window_handles
    driver.switch_to.window(windows[0])
    driver.refresh()
def ConfirmOrders():
    driver.get('https://funpay.com/orders/trade?id=&buyer=&state=paid&game=')
    wait.until(EC.presence_of_element_located(('xpath','//div[@class="tc-date-left"]')))
    orders = driver.find_elements('xpath','//div[@class="tc-date-left"]')
    print(orders)
    print(len(orders))
    for i in range(len(orders)):
        order_time = driver.find_element('xpath',f'(//div[@class="tc-date-left"])[{i+1}]').text
        order = driver.find_element('xpath',f'(//div[@class="tc-order"])[{i+1}]').text
        if 'день' in order_time or 'дн' in order_time or 'нед' in order_time or 'месяц' in order_time:
            driver.find_element('xpath',f'(//a[@class="tc-item info"])[{i}]').click()
            try:
                time.sleep(1)
                driver.find_element('xpath','//div[@class="chat-msg-text"][text() = "подтвердите выполнение заказа"]')
                order_list.append(order)
                driver.back()
            except:
                send_text('подтвердите выполнение заказа')
                order_list.append(order)
                driver.back()
    print(order_list)
    if len(order_list) > 0:
        driver.get('https://funpay.freshdesk.com/ru-RU/support/tickets/new?ticket_form=%D0%BF%D1%80%D0%BE%D0%B1%D0%BB%D0%B5%D0%BC%D0%B0_%D1%81_%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%BE%D0%BC')
        wait.until(EC.presence_of_element_located(('xpath','//a[@class="fw-twitter-btn py-12 rounded"]'))).click()
        wait.until(EC.presence_of_element_located(('xpath', '//input[@id="helpdesk_ticket_custom_field_cf_your_funpay_username_login_name_2914071"]'))).send_keys(Nickname)
        wait.until(EC.presence_of_element_located(('xpath', '//input[@id="helpdesk_ticket_custom_field_cf_order_number_2914071"]'))).send_keys(order_list[1])
        wait.until(EC.presence_of_element_located(('xpath', '(//div[@data-type="select-one"])[2]'))).click()
        wait.until(EC.presence_of_element_located(('xpath', '//div[@data-value="Продавец"]'))).click()
        wait.until(EC.presence_of_element_located(('xpath', '//div[@class="choices__item choices__placeholder choices__item--selectable"]'))).click()
        wait.until(EC.presence_of_element_located(('xpath', '//div[@data-value="Покупатель забыл подтвердить заказ"]'))).click()
        text = " ".join(map(str,order_list))
        print(text)
        driver.execute_script("window.scrollBy(0, 800)")
        time.sleep(1)
        wait.until(EC.presence_of_element_located(('xpath', '//div[@contenteditable="true"]'))).send_keys(f'Пожалуйста подтвердите выполнение заказов: {text}')
        driver.find_element('xpath','(//button[@type="submit"])[2]').click()
    #//div[@class="fr-element fr-view"]
    #подтвердите выполнение заказа
def send_text(text):
    input_element = driver.find_element('xpath', '//textarea[@class="form-control"]')
    driver.execute_script("arguments[0].value = arguments[1];", input_element, text)
    wait.until(EC.element_to_be_clickable(('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()