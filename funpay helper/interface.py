import threading
import time
from time import sleep

from PyQt6.QtCore import  QSize, Qt
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import backend
import os
from datetime import datetime
import json
import sqlite3

file_path = '../funpay helper/data/log.txt'
#spisok = list('Подождите 44 минуты.', 'Подождите 49 минут.', 'Подождите 13 минут.', 'Подождите 3 часа.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 43 минуты.', 'Подождите 49 минут.', 'Подождите 13 минут.', 'Подождите 3 часа.', 'Подождите 43 минуты.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 43 минуты.', 'Подождите 48 минут.', 'Подождите 13 минут.', 'Подождите 3 часа.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 2 часа.', 'Подождите 2 часа.', 'Подождите 2 часа.', 'Подождите 41 минуту.', 'Подождите 2 часа.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 2 часа.', 'Подождите 2 часа.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 2 часа.', 'Подождите 43 минуты.', 'Подождите 44 минуты.', 'Подождите 2 часа.', 'Подождите 35 минут.', 'Подождите 35 минут.', 'Подождите 44 минуты.', 'Подождите 2 часа.', 'Подождите 44 минуты.', 'Подождите 2 часа.', 'Подождите 12 минут.', 'Подождите 44 минуты.')
class LoginThread(QThread):
    login_finished = pyqtSignal()

    def run(self):
        backend.login()
        self.login_finished.emit()  # Сообщаем о завершении входа

def read_text_from_file():
    with open('D:/programs/development/rofls/.venv/funpay helper/data/log.txt', 'r') as f:
        return f.read()
def write_Cookie_to_file(text):
    with open('../funpay helper/data/Cookie.json', 'a') as f:
        f.truncate(0)
        f.write(text + "\n")
def read_Cookie_from_file():
    with open('../funpay helper/data/Cookie.json', 'r') as file:
        data = json.load(file)
        print(data)
        result = '\n'.join(map(str, data))
        return result

def write_Command_to_file(text):
    with open('../funpay helper/data/Commands.json', 'w') as f:
        json.dump(text, f)
def read_command_from_text():
    with open('../funpay helper/data/Commands.json', 'r') as f:
        data = json.load(f)
        return data
thread_active = 0
class UplotsThread(QThread):
    uplots_finished = pyqtSignal()


    def run(self):
        backend.stop = False
        global thread_active
        while backend.stop == False:
            if thread_active == 0 and backend.thread_active == 0 or thread_active == 1 and backend.thread_active == 0:
                thread_active = 1
                sleep(1)
                backend.up_offers()
                thread_active = 0
                self.uplots_finished.emit()  # Сообщаем о завершении поднятия лотов
                time.sleep(20)
                if thread_active == 0 and backend.thread_active == 0:
                    thread_active = 1

class AutoreplyThread(QThread):
    auto_reply_finished = pyqtSignal()
    def run(self):

        global thread_active

        while backend.chat_stop == False:
            if thread_active == 0 and backend.thread_active == 0 or thread_active == 2 and backend == 0:
                thread_active = 2
                backend.auto_reply()
                thread_active = 0
                self.auto_reply_finished.emit()
            else:
                time.sleep(5)
class SteamGuardThread(QThread):
    def run(self):
        backend.Auto_rent()
class ParsingThread(QThread):
    parsing_finished = pyqtSignal()
    def run(self):
        backend.Parsing_lots()
        self.parsing_finished.emit()





class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()



        self.setFixedSize(800, 600)
        self.setStyleSheet('background-color: #1F1F1F; color: #adacab;')
        layoutH = QHBoxLayout()
        layoutV = QVBoxLayout()
        self.Isloggin = False
        self.stacked_widget = QStackedWidget(self)
        # Создание кнопок
        self.home = QPushButton("Home")
        self.home.clicked.connect(self.showUI1)
        button2 = QPushButton("Button 2")
        self.Chat = QPushButton("ЧАТ")
        self.Chat.clicked.connect(self.showUI3)
        self.Cookie = QPushButton("Информация")
        self.Cookie.clicked.connect(self.showUI4)

        self.settings = QPushButton("Настройки")
        self.settings.clicked.connect(self.showUI5)

        self.Logtext = QTextEdit(self)
        self.Logtext.setReadOnly(True)
        self.Logtext.setStyleSheet("""
                    QTextEdit {
                        background-color: #353535;  /* Цвет фона */
                        color: #adacab;              /* Цвет текста */
                        font-family: Arial;          /* Шрифт */
                        font-size: 14px;             /* Размер шрифта */
                        border: 1px solid #adacab;   /* Граница */
                        padding: 5px;               /* Отступы */
                    }
                """)
        self.Uplots = QPushButton()
        self.Uplots.clicked.connect(self.uplotses)
        self.Uplots.setIcon(QIcon('../funpay helper/data/icons/logo'))
        self.Uplots.setCheckable(True)
        self.Uplots.setIconSize(QSize(168, 54))
        self.Uplots.setFixedSize(168, 54)
        self.login_to_site = QPushButton()
        self.login_to_site.setIcon(QIcon('../funpay helper/data/icons/login'))
        self.login_to_site.clicked.connect(self.start_login_thread)
        self.login_to_site.setIconSize(QSize(168, 54))
        self.login_to_site.setFixedSize(168, 54)
        self.Auto_reply = QPushButton()
        self.Auto_reply.setFixedSize(168, 54)
        self.Auto_reply.setIcon(QIcon('../funpay helper/data/icons/autoreply'))
        self.Auto_reply.setIconSize(QSize(168, 54))
        self.Auto_reply.clicked.connect(self.autoreply)
        self.Auto_reply.setCheckable(True)
        self.auto_send_guard = QPushButton()
        self.auto_send_guard.setFixedSize(168, 54)
        self.auto_send_guard.setIcon(QIcon('../funpay helper/data/icons/Guard'))
        self.auto_send_guard.setIconSize(QSize(168, 54))
        self.auto_send_guard.clicked.connect(self.send_guard)
        self.auto_send_guard.setCheckable(True)
        self.Notifications = QPushButton()
        self.Notifications.setFixedSize(168, 54)
        self.Notifications.setIcon(QIcon('../funpay helper/data/icons/Notification'))
        self.Notifications.setIconSize(QSize(168, 54))
        self.Notifications.setCheckable(True)
        self.Notifications.clicked.connect(self.enable_notifications)


        self.MainGrid = QGridLayout()
        HomeGrid = QWidget()
        HomeGrid.setLayout(self.MainGrid)


        self.CookieGrid = QGridLayout()
        cookieGridW = QWidget()
        cookieGridW.setLayout(self.CookieGrid)

        SellerWidget = QWidget()
        SellerWidget.setFixedSize(200,100)
        SellerWidget.setStyleSheet('background-color: #222222; border: 1px solid #252525')
        SellerWidgetLine = QVBoxLayout()
        label1 = QLabel('ИНФОРМАЦИЯ')
        label1.setStyleSheet('font-family: Arial')
        self.Nickname = QLabel('Ник: ?')
        self.Nickname.setStyleSheet('font-family: Arial')
        SellerWidget.setLayout(SellerWidgetLine)
        SellerWidgetLine.addWidget(label1)
        SellerWidgetLine.addWidget(self.Nickname)

        InfoWidget = QWidget()
        InfoWidget.setFixedSize(400, 100)
        InfoWidget.setStyleSheet('border: 2px solid #252525; background-color: #222222')
        InfoWidgetLayout = QHBoxLayout()
        self.status = QLabel('Статус: PRO')
        self.statusEnd = QLabel('Оканчивается: 30.03.2025')
        InfoWidgetLayout.addWidget(self.status)
        InfoWidgetLayout.addWidget(self.statusEnd)
        InfoWidget.setLayout(InfoWidgetLayout)

        SellsWidget = QWidget()
        SellsWidget.setFixedSize(200, 100)
        SellsWidget.setStyleSheet(' background-color: #222222')
        SellsLayoutV = QVBoxLayout()
        self.Sells = QLabel('Закрыто: ?')
        self.refund_sell = QLabel('Возврат: ?')
        self.open_sell = QLabel('Открыто: ?')

        SellsLayoutV.addWidget(QLabel('Продажи (всё время)'))
        SellsLayoutV.addWidget(self.Sells)
        SellsLayoutV.addWidget(self.refund_sell)
        SellsLayoutV.addWidget(self.open_sell)

        SellsWidget.setLayout(SellsLayoutV)

        BalanceWidget = QWidget()

        BalanceWidgetLayout = QVBoxLayout()
        self.Balance = QLabel('Всего: ?')
        BalanceWidget.setFixedSize(200, 100)
        BalanceWidget.setStyleSheet(' background-color: #222222')
        BalanceWidget.setLayout(BalanceWidgetLayout)
        BalanceWidgetLayout.addWidget(QLabel('БАЛАНС'))
        BalanceWidgetLayout.addWidget(self.Balance)


        self.CookieGrid.addWidget(SellerWidget, 1, 0)
        self.CookieGrid.addWidget(InfoWidget, 0, 0)
        self.CookieGrid.addWidget(SellsWidget, 1, 1)
        self.CookieGrid.addWidget(BalanceWidget, 1, 2)


        self.CommandsLayout = QVBoxLayout()
        self.CommandsWidget = QWidget()
        self.CommandsWidget.setFixedSize(750, 300)
        self.CommandsWidget.setLayout(self.CommandsLayout)
        self.TableCommands = QTableWidget()
        self.TableCommands.setColumnCount(2)
        self.TableCommands.setRowCount(10)
        self.TableCommands.horizontalHeaderItem(0)
        self.TableCommands.horizontalHeaderItem(1)
        self.TableCommands.setHorizontalHeaderLabels(["Команда", "Ответ"])
        self.TableCommands.setColumnWidth(0, 400)
        self.TableCommands.setColumnWidth(1, 400)
        self.TableCommands.setMinimumSize(720, 250)
        self.TableCommands.setCornerButtonEnabled(False)
        self.TableCommands.setStyleSheet("""
                            QTableWidget {
                                background-color: #353535;  /* Цвет фона */
                            }
                            
                        """)
        self.TableCommands.setStyleSheet("""
            QTableCornerButton::section {
            background: #353535;
            }
        """)
        self.TableCommands.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #353535; color: #adacab; }")
        self.TableCommands.verticalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #353535; color: #adacab; }")
        self.TableCommands.horizontalHeader().setStretchLastSection(True)
        data = read_command_from_text()
        for row, (key, value) in enumerate(data.items()):
            self.TableCommands.setItem(row, 0, QTableWidgetItem(str(key)))
            self.TableCommands.setItem(row, 1, QTableWidgetItem(str(value)))

        self.CommandsLayout.addWidget(self.TableCommands)

        self.ChatGrid = QGridLayout()
        self.autoreplyLayout = QVBoxLayout()
        self.autoreplyHLayout = QHBoxLayout()
        self.autoreplyLayout.addLayout(self.autoreplyHLayout)
        self.autoreplyWidget = QWidget()
        self.autoreplyWidget.setLayout(self.autoreplyLayout)
        #self.top_widget.setFixedHeight(50)  # Высота верхнего виджета
        self.autoreplyWidget.setStyleSheet("background-color: #1F1F1F; color: #adacab ")
        self.autoreplyEditText = QTextEdit(self)
        self.autoreplyEditText.setReadOnly(False)
        last_autoreplytext = backend.AutoreplyText
        self.autoreplyEditText.setText(last_autoreplytext)
        self.autoreplyEditText.setStyleSheet("""
                                    QTextEdit {
                                        background-color: #353535;  /* Цвет фона */
                                        color: #adacab;              /* Цвет текста */
                                        font-family: Arial;          /* Шрифт */
                                        font-size: 14px;             /* Размер шрифта */
                                        border: 1px solid #adacab;   /* Граница */
                                        padding: 10px;               /* Отступы */
                                    }
                                """)
        self.autoreplyEditTextSave = QPushButton('СОХРАНИТЬ')
        self.autoreplyEditTextSave.setStyleSheet("background-color: #252525")
        self.autoreplyEditTextSave.clicked.connect(self.editTextSave)
        self.infobutton = QPushButton('?',self)
        self.infobutton.setFixedSize(20, 20)
        self.infobutton.setStyleSheet("font-size: 15px;background-color: #1c1404; color: #adacab; ")
        self.infobutton.setToolTip("Бот отвечает только на первое сообщение или если автоответ был изменён \nДля переноса текста на новую строку используйте \\n \n %НИК% - никнейм покупателя")
        self.infobutton.setStyleSheet("QToolTip { background-color: #353535; color: #adacab; border: 1px solid black; }")
        self.infobutton.setCursor(Qt.CursorShape.PointingHandCursor)
        autoreplyTextinfo = QLabel('АВТООТВЕТЧИК')
        self.autoreplyHLayout.addWidget(autoreplyTextinfo)
        self.autoreplyHLayout.addWidget(self.infobutton)
        self.autoreplyLayout.addWidget(self.autoreplyEditText)

        self.changedWidgets = QStackedWidget(self)
        self.changedWidgetLayout = QHBoxLayout()
        self.ChangeWidget1 = QPushButton('Команды')
        self.ChangeWidget1.clicked.connect(self.showWidget1)
        self.ChangeWidget1.setIcon(QIcon('../funpay helper/data/icons/imageCommands'))
        self.ChangeWidget1.setFixedSize(150,30)
        self.ChangeWidget1.setIconSize(QSize(30, 30))
        self.ChangeWidget2 = QPushButton('Оффлайн активации')
        self.ChangeWidget2.setFixedSize(150, 30)
        self.ChangeWidget2.setIcon(QIcon('../funpay helper/data/icons/SteamImage'))
        self.ChangeWidget2.setIconSize(QSize(30, 30))
        self.ChangeWidget2.clicked.connect(self.showWidget2)
        self.ChangeWidget3 = QPushButton('Аренда')
        self.ChangeWidget3.setFixedSize(150, 30)
        self.ChangeWidget3.setIcon(QIcon('../funpay helper/data/icons/SteamImage'))
        self.ChangeWidget3.setIconSize(QSize(30, 30))
        self.ChangeWidget3.clicked.connect(self.showWidget3)
        self.changedWidgetLayout.addWidget(self.ChangeWidget1)
        self.changedWidgetLayout.addWidget(self.ChangeWidget2)
        self.changedWidgetLayout.addWidget(self.ChangeWidget3)


        self.TableLots = QTableWidget()
        self.TableLots.setColumnCount(3)
        self.TableLots.setRowCount(30)
        self.TableLots.setFixedSize(730, 280)
        #self.TableLots.setStyleSheet("QTableWidget{background-color: #353535;}")
        self.TableLots.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #353535; color: #adacab; }")
        self.TableLots.verticalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #353535; color: #adacab; }")
        self.TableLots.setStyleSheet("""
            QTableCornerButton::section {
            background: #353535;
            }
        """)
        self.TableLots.setHorizontalHeaderLabels(["Выданные логин/пароль", "Почта", "Заметки"])



        SteamWidgetLayout = QVBoxLayout()
        SteamWidgetLayout.addWidget(self.TableLots)
        self.TableLots.setColumnWidth(0, 240)
        self.TableLots.setColumnWidth(1, 240)
        self.TableLots.horizontalHeader().setStretchLastSection(True)  # Последняя колонка будет растягиваться
        LotsItems = self.db_getinfo('Steam_Guard')
        lengt = len(LotsItems)
        for i in range(lengt):
            self.TableLots.setItem(i, 0, QTableWidgetItem(LotsItems[i][0]))
            self.TableLots.setItem(i, 1, QTableWidgetItem(LotsItems[i][1]))
            self.TableLots.setItem(i, 2, QTableWidgetItem(LotsItems[i][2]))
            print(LotsItems[i][0])
            print(LotsItems[i][1])
            print(LotsItems[i][2])


        self.SteamWidget = QWidget()
        self.SteamWidget.setLayout(SteamWidgetLayout)
        self.SteamWidget.setFixedSize(750, 300)

        RentWidgetLayout = QVBoxLayout()
        self.Rent_Widget = QWidget()
        self.Rent_Widget.setLayout(RentWidgetLayout)

        RentHorizontalLayout = QHBoxLayout()
        self.parsing_lots = QPushButton('Спарсить лоты')
        self.parsing_lots.clicked.connect(self.StartParsLots)
        self.TableLotsRent = QTableWidget()
        self.TableLotsRent.setColumnCount(3)
        self.TableLotsRent.setRowCount(10)
        self.TableLotsRent.setMinimumSize(720, 250)
        # self.TableLots.setStyleSheet("QTableWidget{background-color: #353535;}")
        self.TableLotsRent.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #353535; color: #adacab; }")
        self.TableLotsRent.verticalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #353535; color: #adacab; }")
        self.TableLotsRent.setStyleSheet("""
                    QTableCornerButton::section {
                    background: #353535;
                    }
                """)
        self.TableLotsRent.setHorizontalHeaderLabels(["Лот", "Логин|Почта", "Время аренды"])
        self.TableLotsRent.setColumnWidth(0, 400)
        self.TableLotsRent.setColumnWidth(1, 200)
        self.TableLotsRent.horizontalHeader().setStretchLastSection(True)

        LotsItems2 = self.db_getinfo('Rent')
        lengt = len(LotsItems2)
        for i in range(lengt):
            self.TableLotsRent.setItem(i, 0, QTableWidgetItem(LotsItems2[i][0]))
            self.TableLotsRent.setItem(i, 1, QTableWidgetItem(LotsItems2[i][1]))
            self.TableLotsRent.setItem(i, 2, QTableWidgetItem(LotsItems2[i][2]))
            print(LotsItems2[i][0])
            print(LotsItems2[i][1])
            print(LotsItems2[i][2])

        RentWidgetLayout.addWidget(self.parsing_lots)
        RentWidgetLayout.addWidget(self.TableLotsRent)
        self.changedWidgets.addWidget(self.CommandsWidget)
        self.changedWidgets.addWidget(self.SteamWidget)
        self.changedWidgets.addWidget(self.Rent_Widget)
        self.changedWidgets.setFixedSize(750, 300)
        self.changedWidgets.setCurrentIndex(0)


        self.ChatGrid.addWidget(self.autoreplyWidget,0,0)
        self.ChatGrid.addWidget(self.autoreplyEditTextSave, 0, 2)
        self.ChatGrid.addLayout(self.changedWidgetLayout, 1,0,)
        self.ChatGrid.addWidget(self.changedWidgets, 3, 0,1,1)
        self.ChatGrid.setRowStretch(3,2)
        self.infobutton.setMouseTracking(True)
        chatGrid = QWidget()
        chatGrid.setLayout(self.ChatGrid)

        self.infobutton2 = QPushButton('?', self)
        self.infobutton2.setFixedSize(20, 20)
        self.infobutton2.setStyleSheet("font-size: 15px;background-color: #1c1404; color: #adacab; ")
        self.infobutton2.setToolTip("""
        Подключение:
        1. Зайдите в тг бота @BotFather
        2. Создайте тг бота написав /newbot
        3.После создания вы получите токен бота, вставьте его в первое поле
        4. Зайдите в созданного тг бота и нажмите старт
        5. Зайдите в тг бота @getmyid_bot
        6. Нажмите Старт, скопируйте ваш chatID и вставьте во второе поле
        7. Проверьте настройки, нажав ПРОВЕРИТЬ
        """)
        self.infobutton2.setStyleSheet(
            "QToolTip { background-color: #353535; color: #adacab; border: 1px solid black; }")
        self.infobutton2.setCursor(Qt.CursorShape.PointingHandCursor)

        self.infobutton3 = QPushButton('?', self)
        self.infobutton3.setFixedSize(20, 20)
        self.infobutton3.setStyleSheet("font-size: 15px;background-color: #1c1404; color: #adacab; ")
        self.infobutton3.setToolTip("""
                Эти поля обязательны для заполнения, без них программа не будет работать.
                Путь к User data указывать через /
                Пример:C:/Users/User/AppData/Local/Google/Chrome/User Data 
                Во второе поле вписать название созданного профиля
                Подробную инструкцию вы можете получить в тг боте нажав на кнопку 'Инструкция' --> 'Первый запуск'
                """)
        self.infobutton3.setStyleSheet(
            "QToolTip { background-color: #353535; color: #adacab; border: 1px solid black; }")
        self.infobutton3.setCursor(Qt.CursorShape.PointingHandCursor)

        SettingsGridWidget = QWidget()
        SettingsGrid = QGridLayout()
        BrowserProfileWidget = QWidget()
        BrowserProfileWidget.setFixedSize(300,200)
        BrowserProfileWidget.setStyleSheet("background-color: #222222")
        BrowserProfileWidgetLayout = QVBoxLayout()
        BrowserProfileWidgetLayoutH = QHBoxLayout()
        BrowserProfileWidgetLayoutH2 = QHBoxLayout()
        BrowserProfileWidgetLayoutH3 = QHBoxLayout()
        self.UserDataTextEdit = QTextEdit()
        self.ProfileDirectoryTextEdit = QTextEdit()
        saveProfileButton = QPushButton('Сохранить')
        saveProfileButton.setStyleSheet("background-color: #252525")
        saveProfileButton.clicked.connect(self.SaveProfileData)
        try:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute("SELECT UserData FROM UserProfile")
            t1 = cursor.fetchone()
            self.UserDataTextEdit.setText(t1[0])
            cursor.execute("SELECT ProfileDirectory FROM UserProfile")
            t2 = cursor.fetchone()
            self.ProfileDirectoryTextEdit.setText(t2[0])
            conn.close()
        except:
            conn.close()


        BrowserProfileWidgetLayout.addLayout(BrowserProfileWidgetLayoutH3)
        BrowserProfileWidgetLayout.addLayout(BrowserProfileWidgetLayoutH)
        BrowserProfileWidgetLayout.addLayout(BrowserProfileWidgetLayoutH2)
        BrowserProfileWidgetLayoutH3.addWidget(QLabel('Настройки входа'))
        BrowserProfileWidgetLayoutH3.addWidget(self.infobutton3)
        BrowserProfileWidgetLayoutH.addWidget(QLabel('User Data'))
        BrowserProfileWidgetLayoutH.addWidget(self.UserDataTextEdit)
        BrowserProfileWidgetLayoutH2.addWidget(QLabel('Profile dir'))
        BrowserProfileWidgetLayoutH2.addWidget(self.ProfileDirectoryTextEdit)
        BrowserProfileWidgetLayout.addWidget(saveProfileButton)
        BrowserProfileWidget.setLayout(BrowserProfileWidgetLayout)

        NotificationWidget = QWidget()
        NotificationWidget.setStyleSheet("background-color: #222222")
        NotificationWidget.setFixedSize(300,200)
        NotificationLayout = QVBoxLayout()
        NotificationLayoutH = QHBoxLayout()
        NotificationLayoutH2 = QHBoxLayout()
        NotificationLayoutH3 = QHBoxLayout()
        NotificationLayoutH3.addWidget(QLabel('УВЕДОМЛЕНИЯ'))
        NotificationLayoutH3.addWidget(self.infobutton2)
        NotificationLayout.addLayout(NotificationLayoutH3)
        NotificationLayout.addLayout(NotificationLayoutH)
        NotificationLayout.addLayout(NotificationLayoutH2)

        self.Telegram_tokenWidget = QTextEdit()
        text_ttw = QLabel('Токен:')
        self.chat_id_widget = QTextEdit()
        try:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute("SELECT Token FROM TGbot")
            t1 = cursor.fetchone()
            self.Telegram_tokenWidget.setText(t1[0])
            cursor.execute("SELECT ID FROM TGbot")
            t2 = cursor.fetchone()
            self.chat_id_widget.setText(t2[0])
            conn.close()
        except:
            conn.close()

        self.message_notification = QCheckBox('Отправлять уведомления о сообщениях')
        self.message_notification.stateChanged.connect(self.on_checkbox_state_changed)
        text_ciw = QLabel('чат id:')
        self.NotificationButton = QPushButton('Проверить')
        self.NotificationButton.clicked.connect(self.testTG)
        NotificationLayoutH.addWidget(text_ttw)
        NotificationLayoutH.addWidget(self.Telegram_tokenWidget)
        NotificationLayoutH2.addWidget(text_ciw)
        NotificationLayoutH2.addWidget(self.chat_id_widget)
        NotificationLayout.addWidget(self.message_notification)
        NotificationLayout.addWidget(self.NotificationButton)
        NotificationWidget.setLayout(NotificationLayout)

        SettingsGrid.addWidget(NotificationWidget,0,1)
        SettingsGrid.addWidget(BrowserProfileWidget, 0,0)
        SettingsGridWidget.setLayout(SettingsGrid)


        # Создание макета
        layoutH.addWidget(self.home)
        layoutH.addWidget(button2)
        layoutH.addWidget(self.Chat)
        layoutH.addWidget(self.Cookie)
        layoutH.addWidget(self.settings)
        layoutV.addLayout(layoutH)
        layoutV.addWidget(self.stacked_widget)
        self.stacked_widget.addWidget(HomeGrid)
        self.stacked_widget.addWidget(chatGrid)
        self.stacked_widget.addWidget(cookieGridW)
        self.stacked_widget.addWidget(SettingsGridWidget)


        # Добавление других кнопок ниже
        self.MainGrid.addWidget(self.Uplots, 1, 0, 1, 1)
        self.MainGrid.addWidget(self.Auto_reply, 2, 0, 1, 1)
        self.MainGrid.addWidget(self.auto_send_guard, 3, 0, 1, 1)
        self.MainGrid.addWidget(self.Notifications, 4, 0, 1, 1)
        self.MainGrid.addWidget(self.login_to_site, 5, 0, 1, 1)
        self.MainGrid.addWidget(self.Logtext, 1, 1, 5, 3 )
        self.stacked_widget.setCurrentIndex(0)
        self.setLayout(layoutV)
        self.setWindowTitle("My App")

        thread_log = threading.Thread(target=self.check_file, args=(file_path,))
        thread_log.start()
    def showWidget1(self):
        self.changedWidgets.setCurrentIndex(0)

    def showWidget2(self):
        self.changedWidgets.setCurrentIndex(1)
    def showWidget3(self):
        self.changedWidgets.setCurrentIndex(2)
    def showUI1(self):
        self.stacked_widget.setCurrentIndex(0)

    def showUI3(self):
        self.stacked_widget.setCurrentIndex(1)
    def showUI4(self):
        self.stacked_widget.setCurrentIndex(2)

    def showUI5(self):
        self.stacked_widget.setCurrentIndex(3)

    def StartParsLots(self):
        self.threatParsing = ParsingThread()
        self.threatParsing.parsing_finished.connect(self.on_parsung_finished)
        self.threatParsing.start()
    def on_checkbox_state_changed(self, state):
        if state == 0:
            backend.SendMessages = False
            print('не отмечен')
        elif state == 2:
            backend.SendMessages = True
            print('отмечен')
    def testTG(self):
        token = self.Telegram_tokenWidget.toPlainText()
        tg_id = self.chat_id_widget.toPlainText()
        if token and tg_id:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS TGbot (Token TEXT NOT NULL, ID TEXT NOT NULL)""")
            cursor.execute("DELETE FROM TGbot")
            cursor.execute("INSERT INTO TGbot VALUES (?, ?)", (token, tg_id))
            cursor.execute("SELECT Token FROM TGbot")
            conn.commit()
            conn.close()
            backend.send_message_to_tgbot('тест')


    def SaveCookie(self):
        length_cookie = len(self.CookieText.toPlainText())
        if length_cookie == 0:
            QMessageBox.warning(
                self,
                'Ошибка',
                'Введите куки',
                QMessageBox.StandardButton.Ok
            )
        else:
            write_Cookie_to_file(self.CookieText.toPlainText())
            QMessageBox.information(
                self,
                'уведомление',
                'Куки сохранены. Перезапустите программу',
                QMessageBox.StandardButton.Ok
            )
            self.close()
    def SaveProfileData(self):
        userdata = self.UserDataTextEdit.toPlainText()
        profiledir = self.ProfileDirectoryTextEdit.toPlainText()
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS UserProfile (UserData TEXT NOT NULL, ProfileDirectory TEXT NOT NULL)""")
        cursor.execute(f"DELETE FROM UserProfile")
        cursor.execute(f"INSERT INTO UserProfile VALUES (?,?)", (userdata,profiledir))
        cursor.execute(f"SELECT * FROM UserProfile")
        print(cursor.fetchall())
        conn.commit()
        conn.close()
        QMessageBox.information(
            self,
            'уведомление',
            'Данные сохранены. Перезапустите программу',
            QMessageBox.StandardButton.Ok
        )
        self.close()

    def editTextSave(self):
        data_dict = {}
        row_count = self.TableCommands.rowCount()
        column_count = self.TableCommands.columnCount()
        try:
            for row in range(row_count):
                key = self.TableCommands.item(row,0).text()
                if key:
                    for column in range(1, column_count):
                            item = self.TableCommands.item(row, column)
                            value = item.text()
                            if value:
                                data_dict[key] = value
        except:
            print('пустая клетка')
        write_Command_to_file(data_dict)
        backend.AutoreplyText = self.autoreplyEditText.toPlainText()
        autoreplytext = self.autoreplyEditText.toPlainText()
        print(autoreplytext)
        autort = 'autort'
        saveData_to_db(autoreplytext, autort)

        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS Steam_Guard (login TEXT NOT NULL, mail TEXT NOT NULL, password TEXT NOT NULL)""")
        cursor.execute(f"DELETE FROM Steam_Guard")


        row_count_lots = self.TableLots.rowCount()
        column_count_lots = self.TableLots.columnCount()

        for row in range(row_count_lots):
                try:
                    key2 = self.TableLots.item(row,0).text()
                    if key2:
                        item1 = self.TableLots.item(row, 1).text()
                        item2 = self.TableLots.item(row, 2).text()
                        print(key2, item1, item2)
                        cursor.execute(f"INSERT INTO Steam_Guard VALUES (?,?,?)", (key2,item1,item2))
                except:
                    None
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS Rent (Lot TEXT NOT NULL, Info TEXT, Time TEXT NOT NULL)""")
        cursor.execute(f"DELETE FROM Rent")
        row_count_rent = self.TableLotsRent.rowCount()
        column_count_rent = self.TableLotsRent.columnCount()
        for row1 in range(row_count_rent):
                try:
                    key3 = self.TableLotsRent.item(row1,0).text()
                    if key3:
                        item3 = self.TableLotsRent.item(row1, 1).text()
                        item4 = self.TableLotsRent.item(row1, 2).text()
                        print(key3, item3, item4)
                        cursor.execute(f"INSERT INTO Rent VALUES (?,?,?)", (key3,item3,item4))
                except:
                    None

        conn.commit()
        conn.close()
        QMessageBox.information(
            self,
            'уведомление',
            'Данные сохранены',
            QMessageBox.StandardButton.Ok
        )
    def db_getinfo(self, name_db):
        db = sqlite3.connect(database)
        c = db.cursor()
        c.execute(f"SELECT * FROM {name_db}")
        text = c.fetchall()
        return text
    def check_file(self, file_path):
        while True:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r+') as file:
                    content = file.read()  # читаем содержимое файла
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    time_ad =  '[' + str(current_time) + ']' + content
                    self.Logtext.append(time_ad)  # выводим содержимое на экран
                    file.truncate(0)  # очищаем файл

    def start_login_thread(self):

        self.login_to_site.setIcon(QIcon('../funpay helper/data/icons/login2'))
        self.login_to_site.setEnabled(False)
        self.login_thread = LoginThread()
        self.login_thread.login_finished.connect(self.on_login_finished)
        self.login_thread.start()

    def on_login_finished(self):
        self.Isloggin = True
        self.Nickname.setText(f'Ник: {backend.Nickname}')
        self.Sells.setText(f'Закрыто: {len(backend.sales)}')
        self.open_sell.setText(f'Открыто: {len(backend.sales_open)}')
        self.refund_sell.setText(f'Возврат: {len(backend.sales_refund)}')
        self.Balance.setText(f'Всего: {backend.Balance}')
    def on_parsung_finished(self):
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        try:
            self.TableLotsRent.setRowCount(len(backend.offers))
            print(backend.offers)
            lines = backend.offers[1].split('\n')
            lenlines = len(lines)
            if lenlines == 3:
                print(f'тест {lines[1]}')
            for i in range(len(backend.offers)):
                lines = backend.offers[i].split('\n')
                lenlines = len(lines)
                if lenlines == 3:
                    line = lines[1]
                elif lenlines == 2:
                    line = lines[0]
                self.TableLotsRent.setItem(i, 0, QTableWidgetItem(line))
                cursor.execute("SELECT Lot FROM Rent")
                Lots = cursor.fetchall()
                try:
                    for j in range(len(Lots)):
                        #print(j)
                        if Lots[j][0] in backend.offers[i]:
                            #print(backend.offers[i])
                            timeT = cursor.execute(f"SELECT Time FROM Rent WHERE Lot = {Lots[j][0]}")
                            timeText = cursor.fetchone()
                            self.TableLotsRent.setItem(i, 2, QTableWidgetItem(timeText[0]))
                except:
                    None
            print(Lots[0][0])
            conn.commit()
            conn.close()

        except:
            conn.commit()
            conn.close()
            print(len(backend.offers))

    def uplotses(self, checked):
        if self.Isloggin == True:
            #thread_log.start()
            if checked:
                print(threading.active_count())
                self.Uplots.setIcon(QIcon('../funpay helper/data/icons/logo2'))
                self.uplots_thread = UplotsThread()
                self.uplots_thread.uplots_finished.connect(self.on_uplots_finished)
                self.uplots_thread.start()

            else:
                print(threading.active_count())
                backend.stop = True
                self.Uplots.setIcon(QIcon('../funpay helper/data/icons/logo'))
        else:
            backend.write_text_to_file('Дождитесь входа в аккаунт')

    def autoreply (self, checked):
        if self.Isloggin == True:
            #thread_log.start()
            if checked:
                backend.chat_stop = False
                self.Auto_reply.setIcon(QIcon('../funpay helper/data/icons/autoreply2'))
                self.Auto_reply_thread = AutoreplyThread()
                self.Auto_reply_thread.auto_reply_finished.connect(self.on_autoreply_finished)
                self.Auto_reply_thread.start()
            else:
                backend.chat_stop = True
                self.Auto_reply.setIcon(QIcon('../funpay helper/data/icons/autoreply'))
                print('Автоответ выключен')


        else:
            backend.write_text_to_file('Дождитесь входа в аккаунт')
    def send_guard(self, checked):
        if self.Isloggin == True:
            if checked:
                backend.AutoGuard = True
                self.auto_send_guard.setIcon(QIcon('../funpay helper/data/icons/Guard2'))
            #self.send_guard_thread =  SteamGuardThread()
            #self.send_guard_thread.start()
            else:
                backend.AutoGuard = False
                self.auto_send_guard.setIcon(QIcon('../funpay helper/data/icons/Guard'))

        #else:
            #backend.write_text_to_file('Для выполнения действия войдите в аккаунт')
    def enable_notifications(self,checked):
        if checked:
            self.Notifications.setIcon(QIcon('../funpay helper/data/icons/Notification2'))
            backend.SendNotifications = True
        else:
            backend.SendNotifications = False
            self.Notifications.setIcon(QIcon('../funpay helper/data/icons/Notification'))

    def on_uplots_finished(self):
        # Здесь можно выполнить дополнительные действия после завершения поднятия лотов
        print("Поднятие лотов завершено.")
    def on_autoreply_finished(self):
        # Здесь можно выполнить дополнительные действия после завершения поднятия лотов
        print("Закончился цикл автоответа")
database = '../funpay helper/data/database.db'
#def create_connection(db_file):
    #conn = sqlite3.connect(db_file)
    #return conn
#database = sqlite3.connect('D:/programs/development/rofls/.venv/funpay helper/data/database.db')
#cursor = database.cursor()
#cursor.execute("""CREATE TABLE IF NOT EXISTS autort (Text TEXT NOT NULL)""")
def saveData_to_db(text, name_db):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name_db} (Text TEXT NOT NULL)""")
    cursor.execute(f"DELETE FROM {name_db}")
    cursor.execute(f"INSERT INTO {name_db} VALUES (?)", (text, ))
    cursor.execute(f"SELECT * FROM {name_db}")
    conn.commit()
    conn.close()
#def lastAutoReplyText():
    #conn = create_connection(database)
    #cursor = conn.cursor()
    #cursor.execute("SELECT * FROM autort")
    #text = cursor.fetchone()
    #text2 = ''.join(map(str, text))
    #print(text2)
    #return text2
    #conn.commit()
    #conn.close()
#//div[@class="tc-desc"]//text()[contains(.,"Аренда")]
app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
