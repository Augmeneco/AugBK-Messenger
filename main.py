#!/usr/bin/python

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QAction, QPalette, QColor
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer, pyqtSignal, QThread, QObject, QSize

import mainwindow, chatwidget, messagewidget
import vkapi

from datetime import datetime
import requests, re, sys, os, traceback, json, threading


class MessageWidget(QtWidgets.QWidget, messagewidget.Ui_Form):
    moveScrollBottom = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def resizeEvent(self, event):
        pass

    def showEvent(self, event):
        self.moveScrollBottom.emit(self.scrollBottom)

class ChatWidget(QtWidgets.QWidget, chatwidget.Ui_Form):
    openChat = pyqtSignal(vkapi.Chat, int, int)

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
        self.openChat.emit(self.chatObject, 20, 0)

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.config = json.loads(open('data/config.json','r').read())
        self.vkapi = vkapi.VK_API(self.config['token'])
        self.activeChat = 0
        self.activeChatOffset = 0
        self.compactMode = False
        self.lastMsgScrollPos = 0
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.msgScrollMoved)
        self.sendMessageButton.clicked.connect(
            lambda: self.sendMessage(self.messageTextLabel.text(), self.activeChat))
        

        QtWidgets.QScroller.grabGesture(self.scrollArea, QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        QtWidgets.QScroller.grabGesture(self.scrollArea_2, QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture)

        self.menuButton.setIcon(QIcon('data/icons/navigation-16-filled.svg'))
        self.menuButton.setIconSize(QSize(32,32))

        self.backButtonCompact.setIcon(QIcon('data/icons/arrow-left-16-filled.svg'))
        self.backButtonCompact.setIconSize(QSize(32,32))

        self.chatInfoButton.setIcon(QIcon('data/icons/navigation-16-filled.svg'))
        self.chatInfoButton.setIconSize(QSize(32,32))

        self.attachButton.setIcon(QIcon('data/icons/attach-16-filled.svg'))
        self.attachButton.setIconSize(QSize(32,32))

        self.sendMessageButton.setIcon(QIcon('data/icons/send-16-filled.svg'))
        self.sendMessageButton.setIconSize(QSize(32,32))

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

    def buildMsgWidget(self, msg: vkapi.Msg):
        messageWidget = MessageWidget()
        messageWidget.msgObject = msg
        messageWidget.avatar.clear()
        messageWidget.avatar.setPixmap(msg.fromId.image)
        messageWidget.text.setText(msg.text)
        messageWidget.date.setText(datetime.utcfromtimestamp(msg.date).strftime("%H:%M:%S"))
        messageWidget.name.setText('<b>{} {}</b>'.format(msg.fromId.firstName, msg.fromId.lastName))
        messageWidget.moveScrollBottom.connect(self.moveMsgScroll)
        
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
        else:
            for reply in msg.reply:
                replyWidget = self.buildMsgWidget(reply)
                messageWidget.replyMsgsLayout.addWidget(replyWidget)

        self.lastMsgScrollPos = self.scrollArea.verticalScrollBar().value()
        if self.scrollArea.verticalScrollBar().value() == self.scrollArea.verticalScrollBar().maximum():
            messageWidget.scrollBottom = True
        else:
            messageWidget.scrollBottom = False

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
                    chat.unread.setStyleSheet('QLabel { background-color: transparent}')

                self.chatsListLayout.insertWidget(0, chat)
                break

    def openChat(self, chatObject: vkapi.Chat, count, offset):
        if offset == 0:
            self.activeChatOffset = 0
            while self.msgsListLayout.count():
                child = self.msgsListLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            threading.Thread(target=self.vkapi.call, args=('messages.markAsRead'), kwargs={'peer_id':chatObject.id}).start()
        msgs = self.vkapi.getHistory(chatObject.id, count, offset)
        for msg in msgs:
            messageWidget = self.buildMsgWidget(msg)
            self.msgsListLayout.insertWidget(0, messageWidget)

        self.chatAvatar.setPixmap(chatObject.image.scaled(32,32))
        self.chatName.setText(chatObject.name)

        self.activeChat = chatObject.id
        self.adaptInterface()

    def sendMessage(self, text: str, peerId: int):
        params = {'message':text,'peer_id':peerId,'random_id':0}
        threading.Thread(target=self.vkapi.call, args=("messages.send",), kwargs=params).start()
        
        self.messageTextLabel.clear()

    def scrollAreaResized(self, event):
        pass

    def newMsgEvent(self, msg: vkapi.Msg):
        if self.activeChat == msg.peerId:
            messageWidget = self.buildMsgWidget(msg)
            self.msgsListLayout.addWidget(messageWidget)
        self.updateChatsList(msg)

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
    
    def moveMsgScroll(self,bottom):
        if bottom:
            self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum()))
        else:
            self.scrollArea.verticalScrollBar().rangeChanged.connect(lambda: self.scrollArea.verticalScrollBar().setValue(self.lastMsgScrollPos))

    def moveMsgOffsetScroll(self, min,max):
        self.lastMsgScrollPos = max-self.lastMsgScrollOffset

        self.scrollArea.verticalScrollBar().setValue(
            self.lastMsgScrollPos
        )

    def msgScrollMoved(self, event):
        if self.scrollArea.verticalScrollBar().value() == 0:
            self.activeChatOffset += 20
            
            self.lastMsgScrollOffset = self.scrollArea.verticalScrollBar().maximum()
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())
            self.openChat(self.vkapi.chatsCache[self.activeChat], 20, self.activeChatOffset)
            
            self.scrollArea.verticalScrollBar().rangeChanged.connect(self.moveMsgOffsetScroll)
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()