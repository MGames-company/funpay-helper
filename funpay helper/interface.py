import threading
import time
from time import sleep

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys
import backend
import os
from datetime import datetime

file_path = 'log.txt'
#spisok = list('Подождите 44 минуты.', 'Подождите 49 минут.', 'Подождите 13 минут.', 'Подождите 3 часа.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 43 минуты.', 'Подождите 49 минут.', 'Подождите 13 минут.', 'Подождите 3 часа.', 'Подождите 43 минуты.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 44 минуты.', 'Подождите 43 минуты.', 'Подождите 48 минут.', 'Подождите 13 минут.', 'Подождите 3 часа.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 2 часа.', 'Подождите 2 часа.', 'Подождите 2 часа.', 'Подождите 41 минуту.', 'Подождите 2 часа.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 2 часа.', 'Подождите 2 часа.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 43 минуты.', 'Подождите 2 часа.', 'Подождите 43 минуты.', 'Подождите 44 минуты.', 'Подождите 2 часа.', 'Подождите 35 минут.', 'Подождите 35 минут.', 'Подождите 44 минуты.', 'Подождите 2 часа.', 'Подождите 44 минуты.', 'Подождите 2 часа.', 'Подождите 12 минут.', 'Подождите 44 минуты.')
class LoginThread(QThread):
    login_finished = pyqtSignal()

    def run(self):
        backend.login()
        time.sleep(5)  # Задержка для симуляции времени входа
        self.login_finished.emit()  # Сообщаем о завершении входа

def read_text_from_file():
    with open('log.txt', 'r') as f:
        return f.read()
def write_Cookie_to_file(text):
    with open('Cookie.txt', 'a') as f:
        f.truncate(0)
        f.write(text + "\n")

class UplotsThread(QThread):
    uplots_finished = pyqtSignal()

    def run(self):
        sleep(1)
        while backend.stop == False:
            backend.up_offers()
            self.uplots_finished.emit()  # Сообщаем о завершении поднятия лотов
            sleep(10)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(800, 600)
        layoutH = QHBoxLayout()
        layoutV = QVBoxLayout()
        self.Isloggin = False
        self.stacked_widget = QStackedWidget(self)
        # Создание кнопок
        self.home = QPushButton("Home")
        self.home.clicked.connect(self.showUI1)
        button2 = QPushButton("Button 2")
        button3 = QPushButton("Button 3")
        self.Cookie = QPushButton("Cookie")
        self.Cookie.clicked.connect(self.showUI4)
        button5 = QPushButton("Настройки")
        self.Logtext = QTextEdit(self)
        self.Logtext.setReadOnly(True)
        self.Logtext.setStyleSheet("""
                    QTextEdit {
                        background-color: #f0f0f0;  /* Цвет фона */
                        color: #333333;              /* Цвет текста */
                        font-family: Arial;          /* Шрифт */
                        font-size: 14px;             /* Размер шрифта */
                        border: 1px solid #cccccc;   /* Граница */
                        padding: 10px;               /* Отступы */
                    }
                """)
        self.Uplots = QPushButton()
        self.Uplots.clicked.connect(self.uplotses)
        self.Uplots.setIcon(QIcon('logo'))
        self.Uplots.setCheckable(True)
        self.Uplots.setIconSize(QSize(168, 54))
        self.Uplots.setFixedSize(168, 54)
        self.login_to_site = QPushButton()
        self.login_to_site.setIcon(QIcon('login'))
        self.login_to_site.clicked.connect(self.start_login_thread)
        self.login_to_site.setIconSize(QSize(168, 54))
        self.login_to_site.setFixedSize(168, 54)
        self.MainGrid = QGridLayout()
        HomeGrid = QWidget()
        HomeGrid.setLayout(self.MainGrid)


        self.CookieGrid = QGridLayout()
        self.CookieText = QTextEdit(self)
        self.CookieText.setReadOnly(False)
        self.CookieText.setStyleSheet("""
                            QTextEdit {
                                background-color: #f0f0f0;  /* Цвет фона */
                                color: #333333;              /* Цвет текста */
                                font-family: Arial;          /* Шрифт */
                                font-size: 14px;             /* Размер шрифта */
                                border: 1px solid #cccccc;   /* Граница */
                                padding: 10px;               /* Отступы */
                            }
                        """)
        self.CookieButton = QPushButton('СОХРАНИТЬ')
        self.CookieButton.clicked.connect(self.SaveCookie)

        self.CookieGrid.addWidget(self.CookieText, 0,0,0,0)
        self.CookieGrid.addWidget(self.CookieButton, 1, 0, 1, 1)
        cookieGridW = QWidget()
        cookieGridW.setLayout(self.CookieGrid)


        # Создание макета
        layoutH.addWidget(self.home)
        layoutH.addWidget(button2)
        layoutH.addWidget(button3)
        layoutH.addWidget(self.Cookie)
        layoutH.addWidget(button5)
        layoutV.addLayout(layoutH)
        layoutV.addWidget(self.stacked_widget)
        self.stacked_widget.addWidget(HomeGrid)
        self.stacked_widget.addWidget(cookieGridW)
        # Добавление других кнопок ниже
        self.MainGrid.addWidget(self.Uplots, 1, 0, 2, 1)
        self.MainGrid.addWidget(self.login_to_site, 2, 0, 2, 1)
        self.MainGrid.addWidget(self.Logtext, 1, 1, 4, 3 )
        self.stacked_widget.setCurrentIndex(0)
        self.setLayout(layoutV)
        self.setWindowTitle("My App")
    def showUI1(self):
            self.stacked_widget.setCurrentIndex(0)
    def showUI4(self):
            self.stacked_widget.setCurrentIndex(1)
    def SaveCookie(self):
        write_Cookie_to_file(self.CookieText.toPlainText())
        QMessageBox.information(
            self,
            'уведомление',
            'Куки сохранены. Перезапустите программу',
            QMessageBox.StandardButton.Ok
        )
        self.close()
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
        self.login_to_site.setIcon(QIcon('login2'))
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
                self.Uplots.setIcon(QIcon('logo2'))
                self.uplots_thread = UplotsThread()
                self.uplots_thread.uplots_finished.connect(self.on_uplots_finished)
                self.uplots_thread.start()
            else:
                backend.stop = True
                self.Uplots.setIcon(QIcon('logo'))
        else:
            backend.write_text_to_file('Дождитесь входа в аккаунт')

    def on_uplots_finished(self):
        # Здесь можно выполнить дополнительные действия после завершения поднятия лотов
        print("Поднятие лотов завершено.")
        print('заново поднимаю лоты')


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
