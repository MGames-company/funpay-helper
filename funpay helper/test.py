import sqlite3
import time


dictinary = {}
if len(dictinary) == 0:
    print('пусто')
dictinary['login'] = [6,0]
dictinary['login2'] = [4,0]
dsf = dictinary.keys()
key = list(dsf)[0]
print(dictinary)
for i in range(6):
    for i in range(len(dictinary)):
        for i in range(len(dictinary)):
            keys = list(dictinary.keys())
            key = keys[i]
            time2 = dictinary.get(key)[1]
            d2 = {key:[dictinary.get(key)[0],time2+1]}
            dictinary.update(d2)
            print(dictinary)
        if dictinary.get(key)[1] > dictinary.get(key)[0]:
            print(key)
            print('Время вышло')
            dictinary.pop(key)
            break
print(dictinary)

"""
Lot = '✅Аренда REPO ✅🟢STEAM🟢💎1 ЧАС 💎'

conn = sqlite3.connect(database)
cursor = conn.cursor()
cursor.execute(f"SELECT Info FROM Rent WHERE Lot = ? ",(Lot,))
info = cursor.fetchone()
info2 = info[0].split('|')
print(info2)
print(len(info2))
if len(info2) == 2:
    login = info2[0]
    mail = info2[1]
    print(f'Mail: {mail} \n login: {login}')
else:
    mail = info2[len(info2)- 1]
    print(mail)  # значение_1
"""

"""
text = "Покупатель Timonvoin174 оплатил заказ #TYAF7VP2. R.E.P.O., Аккаунты, ✅Аренда  REPO ✅🟢STEAM🟢💎1 ЧАС 💎.\nTimonvoin174, не забудьте потом нажать кнопку «Подтвердить выполнение заказа»."
inText = "✅Аренда REPO ✅🟢STEAM🟢💎1 ЧАС 💎"

# Удаляем пробелы из обеих строк
text_no_spaces = text.replace(" ", "")
inText_no_spaces = inText.replace(" ", "")

if inText_no_spaces in text_no_spaces:
    print("внутри")
else:
    print("снаружи")
"""

"""
import os
import sqlite3
import selenium
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.devtools.v85.page import delete_cookie
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("user-data-dir=C:\\Users\\Timon\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument('--profile-directory=Profile 1')
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--window-size=1920,1080')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10, poll_frequency=1)
def split_text(input_text):
    parts = input_text.split('\n')
    print(parts)
    return parts
driver.get('https://funpay.com/chat/?node=158539948')
time.sleep(1)
"""

"""
try:
    zakaz = driver.find_element('xpath','(//a[contains(text(), "заказ")])[last()]').text
    AutoreplyText = f'Спасибо за покупку!\n{zakaz}'
    text_send = split_text(AutoreplyText)
    try:
        for string in text_send:
            print(string)
            driver.find_element('xpath', f'//div[text() = "{string}"]')
    except:
        for string1 in text_send:
            wait.until(EC.presence_of_element_located(('xpath', '//textarea[@class="form-control"]'))).send_keys(string1)
            wait.until( EC.element_to_be_clickable(('xpath', '//button[@type="submit"]/i[@class = \'fa fa-arrow-right\']'))).click()
            driver.refresh()

except:
    print('заказа не было')

time.sleep(3)
"""
"""

def check():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
            wait.until(EC.presence_of_element_located(('xpath', '(//a[contains(text(), "заказ")])[last()]'))).click()
            print('кликнул')
            account = driver.find_element('xpath', '//span[@class="secret-placeholder"]').text
            print(f'выданный аккаунт: {account}')

            cursor.execute("SELECT login FROM Steam_Guard")
            Logins = cursor.fetchall()
            for login in Logins:
                print(login)
                if login[0] in account:
                    print('это оффлайн')
                    type = "Оффлайн"
                    info = 'ничего'
                    return type, info

            h = driver.find_element('xpath','//div[@class="param-item"]/h5[text() = "Краткое описание"]/following-sibling::div').text
            cursor.execute("SELECT Lot FROM Rent")
            Lots = cursor.fetchall()
            for Lot in Lots:
                print(Lot[0])
                if Lot[0] in h:
                    print(f"Это аренда, {Lot[0]}")
                    cursor.execute(f"SELECT Info FROM Rent WHERE Lot = ?", (Lot[0],))
                    info = cursor.fetchone()
                    print(info[0])
                    if info[0]:
                        type = 'Аренда'
                        print(f'Тип: {type}')
                        return type, info[0]
                    else:
                        print('На этот лот не установлена функция автовыдачи')
                        type = 'None'
                        inf = 'ничего'
                        return type, inf
            type = 'ничего'
            inf = 'ничего'
            return type, inf
    except:
            print('Что-то пошло не так')
    conn.close()

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
    try:
        time.sleep(3)
        wait.until(EC.presence_of_element_located(('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')))
        s = driver.find_element('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')
        if s:
            s.click()
        else:
            print('не найден элемент')
        guard = wait.until(EC.presence_of_element_located(('xpath', '(//td[@class="title-48_mr_css_attr c-blue1_mr_css_attr fw-b_mr_css_attr a-center_mr_css_attr"])[1]'))).text
        driver.switch_to.window(windows[0])
        text = f'Код для входа в аккаунт: {guard}'
    except:
        print('!!!ошибка!!!')
    #return guard

    print(text)
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

    db = sqlite3.connect('../funpay helper/data/database.db')
    c = db.cursor()
    c.execute(f"SELECT mail FROM Steam_Guard WHERE login = '{login}'")
    mail = c.fetchone()
    print(mail[0])
    time.sleep(3)
    try:
        wait.until(EC.presence_of_element_located(('xpath',f'//img[@alt="{mail[0]}"]')))
    except:
        driver.find_element('xpath','//div[@class="ph-project__user-icon svelte-ttryjx"]').click()
        wait.until(EC.presence_of_element_located(('xpath',f'//div[text() = "{mail[0]}"]'))).click()
    time.sleep(3)
    wait.until(EC.presence_of_element_located(('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')))
    s = driver.find_element('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')
    if s:
        s.click()
    else:
        print('не найден элемент')
    guard = wait.until(EC.presence_of_element_located(('xpath', '(//td[@class="title-48_mr_css_attr c-blue1_mr_css_attr fw-b_mr_css_attr a-center_mr_css_attr"])[1]'))).text
    driver.switch_to.window(windows[0])
    text = f'Код для входа в аккаунт {login}: {guard}'
    #return guard
    print(text)
    db.close()
type, info = check()
if type == 'Оффлайн':
    db = sqlite3.connect('../funpay helper/data/database.db')
    c = db.cursor()
    c.execute("SELECT login FROM Steam_Guard")
    logins = c.fetchall()
    for login in logins:
        try:
            print(login[0])
            driver.find_element('xpath', f'//div[@class="chat-msg-text"][contains(text(), "{login[0]}")]')
            auto_send_guard(login[0])
        except:
            windows = driver.window_handles
            driver.switch_to.window(windows[0])
            print('ненаход')
elif type == 'Аренда':
    print(type)
    info1 = info.split('|')
    print(info1[1])
    auto_send_guard_rent(info1[1])

time.sleep(60)
"""







#//a[contains(text(), 'заказ')]
#//div[contains(text(), 'Аренда')].text



#Создание таблицы
#c.execute(CREATE TABLE articles (
#    title text,
#    full_text text,
#    views integer,
#    avtor text
#)

#Добавление данных
#c.execute("INSERT INTO articles VALUES ('sad', 'Faceddsabook pizdasadto', 330, 'pidodsar')")


#получение данных

#удаление данных
#c.execute("DELETE FROM articles WHERE rowid = 1")

