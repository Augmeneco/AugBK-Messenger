from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, pyqtSignal, QThread, QObject

import mainwindow
import vkapi

import requests, re, sqlite3, sys, os, traceback, json

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.config = json.loads(open('data/config.json','r').read())

        self.vkapi = vkapi.VK_API(self.config['token'])

        self.lpThread = QThread()

        self.longpoll = vkapi.LongPoll(self.vkapi)
        self.longpoll.moveToThread(self.lpThread)
        self.longpoll.newMsg.connect(self.getnewmsg)
        
        self.lpThread.started.connect(self.longpoll.start)
        self.lpThread.start()

    def getnewmsg(self, msg):
        print(msg)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()