from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, pyqtSignal, QThread, QObject

import mainwindow, chatwidget
import vkapi

from datetime import datetime
import requests, re, sqlite3, sys, os, traceback, json


class ChatWidget(QtWidgets.QWidget, chatwidget.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.config = json.loads(open('data/config.json','r').read())

        self.vkapi = vkapi.VK_API(self.config['token'])

        chats = self.vkapi.getChats(20)
        for chat in chats:
            chatWidget = ChatWidget()
            chatWidget.image.clear()
            chatWidget.image.setPixmap(chat.image)
            chatWidget.name.setText('<b>'+chat.name+'</b>')
            chatWidget.text.setText('{}: {}'.format(
                chat.previewMsg.fromId.firstName, chat.previewMsg.text)
            )
            chatWidget.time.setText(datetime.now().strftime("%H:%M:%S"))
            chatWidget.unread.setText('<b>0</b>')

            self.chatsListLayout.addWidget(chatWidget)

        self.lpThread = QThread()
        self.longpoll = vkapi.LongPoll(self.vkapi)
        self.longpoll.moveToThread(self.lpThread)
        self.longpoll.newMsg.connect(self.getnewmsg)
        
        self.lpThread.started.connect(self.longpoll.start)
        self.lpThread.start()

    def resizeEvent(self, event):
        #self.chatsListWidget.setFixedHeight(self.scrollArea_2.height())
        self.chatsListWidget.setFixedWidth(self.scrollArea_2.width()-24)

        QtWidgets.QMainWindow.resizeEvent(self, event)
        
    def showEvent(self, event):
        self.chatsListWidget.setFixedWidth(self.scrollArea_2.width()-24)

    def getnewmsg(self, msg):
        print(msg)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()