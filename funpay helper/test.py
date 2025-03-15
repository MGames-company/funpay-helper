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

driver.get('https://e.mail.ru/inbox/')

time.sleep(3)

s = driver.find_element('xpath','(//span[text() = "Ваш аккаунт Steam: доступ с нового компьютера"] | //span[text() = "Your Steam account: Access from new computer"])')
if s:
    print('zaebic')
    s.click()
else:
    print('не найдено')

time.sleep(60)








#//a[contains(text(), 'заказ')]
#//div[contains(text(), 'Аренда')].text
"""
db = sqlite3.connect('test.db')

c = db.cursor()

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
c.execute("SELECT rowid, * FROM articles")

#удаление данных
#c.execute("DELETE FROM articles WHERE rowid = 1")

#изменение данных
#c.execute("UPDATE articles SET avtor = 'admin' WHERE title = 'Facebook'")
items = c.fetchall()
print(items)
db.commit()
db.close()
"""