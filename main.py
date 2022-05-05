#!/usr/bin/python

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QAction, QPalette, QColor
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer, pyqtSignal, QThread, QObject

import mainwindow, chatwidget, messagewidget
import vkapi

from datetime import datetime
import requests, re, sqlite3, sys, os, traceback, json


class MessageWidget(QtWidgets.QWidget, messagewidget.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def resizeEvent(self, event):
        pass


class ChatWidget(QtWidgets.QWidget, chatwidget.Ui_Form):
    openChat = pyqtSignal(vkapi.Chat)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.palette = QPalette()
        self.palette.setColor(self.palette.ColorRole.Window, QColor(245, 246, 248))

    def enterEvent(self, event):
        self.setAutoFillBackground(True)
        self.setPalette(self.palette)
        #self.setStyleSheet('QWidget { background-color: #f5f6f8 }')
        
    def leaveEvent(self, event):
        self.setStyleSheet('QWidget { background-color: transparent }')

    def mouseReleaseEvent(self, event):
        self.openChat.emit(self.chatObject)

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.config = json.loads(open('data/config.json','r').read())
        self.vkapi = vkapi.VK_API(self.config['token'])
        self.activeChat = 0
        self.compactMode = False

        chats = self.vkapi.getChats(100)
        for chat in chats:
            chatWidget = ChatWidget()
            chatWidget.image.clear()
            chatWidget.image.setPixmap(chat.image)
            chatWidget.name.setText('<b>'+chat.name+'</b>')
            chatWidget.chatObject = chat

            text = '{}: {}'.format(chat.previewMsg.fromId.firstName, chat.previewMsg.text)[:24]
            if len(text) == 24: text += '...'

            chatWidget.text.setText(text)
            chatWidget.time.setText(datetime.utcfromtimestamp(chat.previewMsg.date).strftime("%H:%M:%S"))

            if chat.unread != 0:
                chatWidget.unread.setText('<b>'+str(chat.unread)+'</b>')
                chatWidget.unread.setStyleSheet('QLabel { background-color: #99a2ad; color: white; margin: 2}')
            else:
                chatWidget.unread.clear()

            chatWidget.openChat.connect(self.openChat)

            self.chatsListLayout.addWidget(chatWidget)

        self.scrollArea.resizeEvent = self.scrollAreaResized
        self.splitter.splitterMoved.connect(self.splitterMoved)

        self.backButtonCompact.clicked.connect(self.backButtonCompactClicked)
        self.backButtonCompact.hide()

        self.lpThread = QThread()
        self.longpoll = vkapi.LongPoll(self.vkapi)
        self.longpoll.moveToThread(self.lpThread)
        self.longpoll.newMsg.connect(self.newMsgEvent)
        
        self.lpThread.started.connect(self.longpoll.start)
        self.lpThread.start()

    def resizeEvent(self, event):
        self.resizeGuiElements()

        if self.width() < self.height():
            self.compactMode = True
        else:
            self.compactMode = False
        
        self.adaptInterface()
            
    def adaptInterface(self):
        if self.compactMode:
            self.backButtonCompact.show()
            if self.activeChat != 0:
                self.splitter.moveSplitter(0,1)
            else:
                self.splitter.moveSplitter(self.scrollArea_2.width()+self.scrollArea.width(), 1)
        else:
            self.backButtonCompact.hide()
            self.splitter.moveSplitter(300,1)

    def backButtonCompactClicked(self):
        self.activeChat = 0
        self.adaptInterface()

    def showEvent(self, event):
        self.resizeGuiElements()
        self.splitter.moveSplitter(300,1)
        self.adaptInterface()

    def resizeGuiElements(self):
        self.chatsListWidget.setFixedWidth(self.scrollArea_2.width()-24)
        self.msgsListWidget.setFixedWidth(self.scrollArea.width()-24)

    def splitterMoved(self, pos, index):
        self.resizeGuiElements()

    def buildMsgWidget(self, msg: vkapi.Msg):
        messageWidget = MessageWidget()
        messageWidget.avatar.clear()
        messageWidget.avatar.setPixmap(msg.fromId.image)
        messageWidget.text.setText(msg.text)
        messageWidget.date.setText(datetime.utcfromtimestamp(msg.date).strftime("%H:%M:%S"))
        messageWidget.name.setText('<b>{} {}</b>'.format(msg.fromId.firstName, msg.fromId.lastName))
        
        if len(msg.attachments) == 0:
            messageWidget.imagesWidget.hide()
        else:
            hasImageAttaches = False
            row = 0
            col = 0
            for attach in msg.attachments: 
                if attach.attachType == vkapi.AttachTypes.STICKER:
                    messageWidget.text.clear()
                    messageWidget.text.setPixmap(attach.preview.scaled(128,128))
                    messageWidget.text.setMinimumSize(128,128)
                    

                if attach.attachType == vkapi.AttachTypes.PHOTO:
                    hasImageAttaches = True
                    image = QtWidgets.QLabel(self)
                    image.setPixmap(attach.preview.scaledToWidth(220))

                    if col == 2: 
                        col = 0
                        row += 1
                    messageWidget.imagesLayout.addWidget(image, row, col)
                    col += 1


            if not hasImageAttaches: messageWidget.imagesWidget.hide()
        
        if len(msg.reply) == 0:
            messageWidget.replyMsgsWidget.hide()

        return messageWidget

    def updateChatsList(self, msg: vkapi.Msg):
        widgets = (self.chatsListLayout.itemAt(i).widget() for i in range(self.chatsListLayout.count())) 

        for chat in widgets:
            if chat.chatObject.id == msg.peerId:
                index = self.chatsListLayout.indexOf(chat)

                chat.chatObject.previewMsg = msg

                if msg.peerId != self.activeChat:
                    chat.chatObject.unread += 1
                else:
                    chat.chatObject.unread = 0

                text = '{}: {}'.format(chat.chatObject.previewMsg.fromId.firstName, chat.chatObject.previewMsg.text)[:24]
                if len(text) == 24: text += '...'

                chat.text.setText(text)
                chat.time.setText(datetime.utcfromtimestamp(chat.chatObject.previewMsg.date).strftime("%H:%M:%S"))

                if chat.chatObject.unread != 0:
                    chat.unread.setText('<b>'+str(chat.chatObject.unread)+'</b>')
                    chat.unread.setStyleSheet('QLabel { background-color: #99a2ad; color: white; margin: 2}')
                else:
                    chat.unread.clear()

                self.chatsListLayout.insertWidget(0, chat)
                break

    def openChat(self, chatObject: vkapi.Chat):
        while self.msgsListLayout.count():
            child = self.msgsListLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.vkapi.call('messages.markAsRead',peer_id = chatObject.id) #todo сделать отрисовку того что прочитано

        msgs = self.vkapi.getHistory(chatObject.id, 20)
        msgs.reverse()
        for msg in msgs:
            messageWidget = self.buildMsgWidget(msg)
            self.msgsListLayout.addWidget(messageWidget)

        self.activeChat = chatObject.id
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
        self.adaptInterface()

    def scrollAreaResized(self, event):
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

    def newMsgEvent(self, msg: vkapi.Msg):
        if self.activeChat == msg.peerId:
            messageWidget = self.buildMsgWidget(msg)
            self.msgsListLayout.addWidget(messageWidget)
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
        self.updateChatsList(msg)
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()