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

file_path = 'D:/programs/development/rofls/.venv/funpay helper/data/log.txt'
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
    with open('D:/programs/development/rofls/.venv/funpay helper/data/Cookie.json', 'a') as f:
        f.truncate(0)
        f.write(text + "\n")
def read_Cookie_from_file():
    with open('D:/programs/development/rofls/.venv/funpay helper/data/Cookie.json', 'r') as file:
        data = json.load(file)
        print(data)
        result = '\n'.join(map(str, data))
        return result

def write_Command_to_file(text):
    with open('D:/programs/development/rofls/.venv/funpay helper/data/Commands.json', 'w') as f:
        json.dump(text, f)
def read_command_from_text():
    with open('D:/programs/development/rofls/.venv/funpay helper/data/Commands.json', 'r') as f:
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
        backend.chat_stop = False
        while backend.chat_stop == False:
            if thread_active == 0 and backend.thread_active == 0:
                thread_active = 2
                print('Автоответ включён')
                backend.auto_reply()
                thread_active = 0
                self.auto_reply_finished.emit()






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
        self.Cookie = QPushButton("Cookie")
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
                        padding: 10px;               /* Отступы */
                    }
                """)
        self.Uplots = QPushButton()
        self.Uplots.clicked.connect(self.uplotses)
        self.Uplots.setIcon(QIcon('D:/programs/development/rofls/.venv/funpay helper/data/icons/logo'))
        self.Uplots.setCheckable(True)
        self.Uplots.setIconSize(QSize(168, 54))
        self.Uplots.setFixedSize(168, 54)
        self.Uplots.setStyleSheet("QPushButton { background-color: #1F1F1F; }" "QPushButton:pressed { background-color: #353535; }")
        self.login_to_site = QPushButton()
        self.login_to_site.setIcon(QIcon('D:/programs/development/rofls/.venv/funpay helper/data/icons/login'))
        self.login_to_site.clicked.connect(self.start_login_thread)
        self.login_to_site.setIconSize(QSize(168, 54))
        self.login_to_site.setFixedSize(168, 54)
        self.Auto_reply = QPushButton()
        self.Auto_reply.setFixedSize(168, 54)
        self.Auto_reply.setIcon(QIcon('D:/programs/development/rofls/.venv/funpay helper/data/icons/autoreply'))
        self.Auto_reply.setIconSize(QSize(168, 54))
        self.Auto_reply.clicked.connect(self.autoreply)
        self.Auto_reply.setCheckable(True)
        self.MainGrid = QGridLayout()
        HomeGrid = QWidget()
        HomeGrid.setLayout(self.MainGrid)


        self.CookieGrid = QGridLayout()
        self.CookieText = QTextEdit(self)
        self.CookieText.setReadOnly(False)
        lastCookieText = read_Cookie_from_file()

        self.CookieText.setText(lastCookieText)
        self.CookieText.setStyleSheet("""
                            QTextEdit {
                                background-color: #353535;  /* Цвет фона */
                                color: #adacab;              /* Цвет текста */
                                font-family: Arial;          /* Шрифт */
                                font-size: 14px;             /* Размер шрифта */
                                border: 1px solid #adacab;   /* Граница */
                                padding: 10px;               /* Отступы */
                            }
                        """)
        self.CookieButton = QPushButton('СОХРАНИТЬ')
        self.CookieButton.clicked.connect(self.SaveCookie)
        self.CookieGrid.addWidget(self.CookieText, 0,0,0,0)
        self.CookieGrid.addWidget(self.CookieButton, 1, 0, 1, 1)
        cookieGridW = QWidget()
        cookieGridW.setLayout(self.CookieGrid)

        self.TableCommands = QTableWidget()
        self.TableCommands.setColumnCount(2)
        self.TableCommands.setRowCount(10)
        self.TableCommands.horizontalHeaderItem(0)
        self.TableCommands.horizontalHeaderItem(1)
        self.TableCommands.setHorizontalHeaderLabels(["Команда", "Ответ"])
        self.TableCommands.setColumnWidth(0, 400)
        self.TableCommands.setColumnWidth(1, 400)
        self.TableCommands.setMinimumSize(700, 300)
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
        self.infobutton.setToolTip("Для переноса текста на новую строку используйте \\n")
        self.infobutton.setStyleSheet("QToolTip { background-color: #353535; color: #adacab; border: 1px solid black; }")
        self.infobutton.setCursor(Qt.CursorShape.PointingHandCursor)
        autoreplyTextinfo = QLabel('АВТООТВЕТЧИК')
        self.autoreplyHLayout.addWidget(autoreplyTextinfo)
        self.autoreplyHLayout.addWidget(self.infobutton)
        self.autoreplyLayout.addWidget(self.autoreplyEditText)




        #QToolTip.setStyleSheet("QToolTip { background-color: #181818; color: black; border: 1px solid black; }")
        self.ChatGrid.addWidget(self.autoreplyWidget,0,0)
        #self.settingsGrid.addWidget(autoreplyTextinfo, 0, 0)
        #self.settingsGrid.addWidget(self.autoreplyEditText, 1,0, 1, 2)
        #self.autoreplyLayout.addWidget(self.top_widget)
        #self.autoreplyLayout.addWidget(autoreplyTextinfo)
        #self.autoreplyLayout.addWidget(self.autoreplyEditText)
        self.ChatGrid.addWidget(self.autoreplyEditTextSave, 0, 2)
        #self.settingsGrid.addWidget(self.infobutton, 0, 1)
        self.ChatGrid.addWidget(self.TableCommands, 3, 0,0,0)
        self.ChatGrid.setRowStretch(3,1)
        self.infobutton.setMouseTracking(True)
        chatGrid = QWidget()
        chatGrid.setLayout(self.ChatGrid)

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

        # Добавление других кнопок ниже
        self.MainGrid.addWidget(self.Uplots, 1, 0, 1, 1)
        self.MainGrid.addWidget(self.Auto_reply, 2, 0, 1, 1)
        self.MainGrid.addWidget(self.login_to_site, 3, 0, 1, 1)
        self.MainGrid.addWidget(self.Logtext, 1, 1, 4, 3 )
        self.stacked_widget.setCurrentIndex(0)
        self.setLayout(layoutV)
        self.setWindowTitle("My App")

    def showUI1(self):
        self.stacked_widget.setCurrentIndex(0)

    def showUI3(self):
        self.stacked_widget.setCurrentIndex(1)
    def showUI4(self):
        self.stacked_widget.setCurrentIndex(2)

    def showUI5(self):
        self.stacked_widget.setCurrentIndex(3)

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
        saveData_to_db(autoreplytext)

        QMessageBox.information(
            self,
            'уведомление',
            'Данные сохранены',
            QMessageBox.StandardButton.Ok
        )
    def check_file(self, file_path):
        while True:
            time.sleep(1)  # ждем 1 секунду
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r+') as file:
                    content = file.read()  # читаем содержимое файла
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    time_ad =  '[' + str(current_time) + ']' + content
                    self.Logtext.append(time_ad)  # выводим содержимое на экран
                    file.truncate(0)  # очищаем файл

    def start_login_thread(self):
        thread_log = threading.Thread(target=self.check_file, args=(file_path,))
        thread_log.start()
        self.login_to_site.setIcon(QIcon('D:/programs/development/rofls/.venv/funpay helper/data/icons/login2'))
        self.login_to_site.setEnabled(False)
        self.login_thread = LoginThread()
        self.login_thread.login_finished.connect(self.on_login_finished)
        self.login_thread.start()

    def on_login_finished(self):
        self.Isloggin = True
        backend.write_text_to_file('Успешный вход')

    def uplotses(self, checked):
        if self.Isloggin == True:
            #thread_log.start()
            if checked:
                print(threading.active_count())
                self.Uplots.setIcon(QIcon('D:/programs/development/rofls/.venv/funpay helper/data/icons/logo2'))
                self.uplots_thread = UplotsThread()
                self.uplots_thread.uplots_finished.connect(self.on_uplots_finished)
                self.uplots_thread.start()

            else:
                print(threading.active_count())
                backend.stop = True
                self.Uplots.setIcon(QIcon('D:/programs/development/rofls/.venv/funpay helper/data/icons/logo'))
        else:
            backend.write_text_to_file('Дождитесь входа в аккаунт')
    def autoreply (self, checked):
        if self.Isloggin == True:
            #thread_log.start()
            if checked:
                self.Auto_reply.setIcon(QIcon('D:/programs/development/rofls/.venv/funpay helper/data/icons/autoreply2'))
                self.Auto_reply = AutoreplyThread()
                self.Auto_reply.auto_reply_finished.connect(self.on_autoreply_finished)
                self.Auto_reply.start()
            else:
                self.Auto_reply.setIcon(QIcon('D:/programs/development/rofls/.venv/funpay helper/data/icons/autoreply'))
                backend.chat_stop = True
                print('Автоответ выключен')
        else:
            backend.write_text_to_file('Дождитесь входа в аккаунт')
    def on_uplots_finished(self):
        # Здесь можно выполнить дополнительные действия после завершения поднятия лотов
        print("Поднятие лотов завершено.")
    def on_autoreply_finished(self):
        # Здесь можно выполнить дополнительные действия после завершения поднятия лотов
        print("Закончился цикл автоответа")
database = 'D:/programs/development/rofls/.venv/funpay helper/data/database.db'
#def create_connection(db_file):
    #conn = sqlite3.connect(db_file)
    #return conn
#database = sqlite3.connect('D:/programs/development/rofls/.venv/funpay helper/data/database.db')
#cursor = database.cursor()
#cursor.execute("""CREATE TABLE IF NOT EXISTS autort (Text TEXT NOT NULL)""")
def saveData_to_db(text):
    conn = create_connection(database)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS autort (Text TEXT NOT NULL)""")
    cursor.execute("DELETE FROM autort")
    cursor.execute("INSERT INTO autort VALUES (?)", (text, ))
    cursor.execute("SELECT * FROM autort")
    LOG = cursor.fetchall()
    print(LOG)
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

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
