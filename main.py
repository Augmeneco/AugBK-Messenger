#!/usr/bin/python

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon, QAction, QPalette, QColor
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QTimer, pyqtSignal, QThread, QThreadPool, QObject, QSize, Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView

import mainwindow, chatwidget, messagewidget
import vkapi, asyncvkapi

from datetime import datetime
from enum import IntEnum
import requests, re, sys, os, traceback, json, threading

class StackedWindows(IntEnum):
    ChatsWindow = 0
    AuthByWebEngine = 1
    AuthByToken = 2
    ImagePreview = 3
    
class MessageWidget(QtWidgets.QWidget, messagewidget.Ui_Form):
    moveScrollBottom = pyqtSignal(bool)
    messageClicked = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def mousePressEvent(self, event):
        self.messageClicked.emit(self)

    #def resizeEvent(self, event):
    #    pass

    #def showEvent(self, event):
    #    pass

class ClickableAttachWidget(QtWidgets.QLabel):
    attachClicked = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        self.attachClicked.emit(self.attachObject)
        

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
        self.openChat.emit(self.chatObject, 50, 0)

class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.threadPool = QThreadPool()
        self.initComplete = False
        self.compactMode = False
        self.lastSplitterPos = 300
        #self.stackedWidget.setCurrentIndex(StackedWindows.ChatsWindow)
        if not os.path.exists('data/config.json'):
            self.stackedWidget.setCurrentIndex(StackedWindows.AuthByWebEngine)
            self.webEngineView.urlChanged.connect(self.authUrlChanged)
            self.webEngineView.setUrl(QUrl('https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=mobile&response_type=token&revoke=1'))
            self.authByTokenButton2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(StackedWindows.AuthByToken))
            self.authByTokenButton.clicked.connect(lambda: self.authByToken(self.authByTokenEdit.text(), direct=True))
        else:
            self.initMainWindow()
    
    def authByToken(self, token, direct=False):
        if ('access_token=' in token):
            token = re.findall('access_token=(.+?)&',token)[0]
        elif not direct: return

        open('data/config.json','w').write(json.dumps({
            'token':token
        }))
        self.stackedWidget.setCurrentIndex(StackedWindows.ChatsWindow)
        self.initMainWindow()

    def authUrlChanged(self, url):
        self.authByToken(url.toString())

    def initMainWindow(self):
        self.webEngineView.deleteLater()
        self.config = json.loads(open('data/config.json','r').read())
        self.vkapi = vkapi.VK_API(self.config['token'])
        self.vkapi.newDebugMessage.connect(self.logging)

        self.activeChat = 0
        self.activeChatOffset = 0
        self.newChatOpened = False

        self.sendMessageButton.clicked.connect(
            lambda: self.sendMessage(self.messageTextEdit.toPlainText(), self.activeChat, **self.sendMessageParams))
        self.messageTextEdit.keyPressEvent = self.messageTextEditEnterHandler

        QtWidgets.QScroller.grabGesture(self.scrollArea.viewport(), QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        QtWidgets.QScroller.grabGesture(self.scrollArea_2.viewport(), QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture)

        #отключение кинетической энерции в тачевом скролле

        #for scrollObj in [self.scrollArea, self.scrollArea_2]:
        #    scrollerProperties = QtWidgets.QScroller.scroller(scrollObj).scrollerProperties()
        #    scrollerProperties.setScrollMetric(QtWidgets.QScrollerProperties.ScrollMetric.MaximumVelocity, 0)
        #    scrollerProperties.setScrollMetric(QtWidgets.QScrollerProperties.ScrollMetric.MinimumVelocity, 0)
        #    QtWidgets.QScroller.scroller(scrollObj).setScrollerProperties(scrollerProperties)

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

        self.emojiButton.setIcon(QIcon('data/icons/emoji-16-regular.svg'))
        self.emojiButton.setIconSize(QSize(32,32))

        getChatsAsync = asyncvkapi.AsyncVKAPI(self.vkapi, 'getChats', count=100)
        getChatsAsync.signals.getChats.connect(self.getChats)
        self.threadPool.start(getChatsAsync)
        self.chatName.setText('Загрузка')

        #self.scrollArea.resizeEvent = self.scrollAreaResized
        self.splitter.splitterMoved.connect(self.splitterMoved)

        self.scrollArea.verticalScrollBar().valueChanged.connect(self.scrollMsgsMoved)
        self.scrollArea.verticalScrollBar().rangeChanged.connect(self.scrollMsgsChanged)
        self.needScrollBottom = True
        self.needOffsetScroll = False
        self.lastMsgScrollPosition = 0
        self.lastMsgScrollMaximum = 0

        self.replyMsgsList = []
        self.replyMsgButton.clicked.connect(self.replyMsgButtonClicked)

        self.sendMessageParams = {}

        self.attachMenuWidget.hide()

        self.backButtonCompact.clicked.connect(self.backButtonCompactClicked)
        self.backButtonCompact.hide()

        self.lpThread = QThread()
        self.longpoll = vkapi.LongPoll(self.vkapi)
        self.longpoll.moveToThread(self.lpThread)
        self.longpoll.newMsg.connect(self.newMsgEvent)
        
        self.lpThread.started.connect(self.longpoll.start)
        self.lpThread.start()

        self.initComplete = True
        self.adaptInterface()

    def getChats(self, chats):
        self.chatName.clear()
        for chat in chats:
            chatWidget = ChatWidget()
            chatWidget.image.clear()
            chatWidget.image.setPixmap(chat.image)
            chatWidget.name.setText('<b>'+chat.name+'</b>')
            chatWidget.chatObject = chat

            text = '{}: {}'.format(chat.previewMsg.fromId.firstName, chat.previewMsg.text)[:24]
            if len(text) == 24: text += '...'

            chatWidget.text.setText(self.vkapi.improveMsgText(text))
            chatWidget.time.setText(datetime.fromtimestamp(chat.previewMsg.date).strftime("%H:%M:%S"))

            if chat.unread != 0:
                chatWidget.unread.setText('<b>'+str(chat.unread)+'</b>')
                chatWidget.unread.setStyleSheet('QLabel { background-color: #99a2ad; color: white; margin: 2}')
            else:
                chatWidget.unread.clear()

            chatWidget.openChat.connect(self.openChat)

            self.chatsListLayout.addWidget(chatWidget)

    def messageTextEditEnterHandler(self, event):
        if event.key() == 16777220:
            self.sendMessage(self.messageTextEdit.toPlainText(), self.activeChat, **self.sendMessageParams)
        else:
            QtWidgets.QPlainTextEdit.keyPressEvent(self.messageTextEdit, event)

    def openImageViewer(self, attach):
        self.stackedWidget.setCurrentIndex(StackedWindows.ImagePreview)
        imageAttach = self.vkapi.loadAttach(attach.name, vkapi.AttachTypes.PHOTO, attach.url)

        if imageAttach.width() >= self.imagePreviewWindow.width():
            sizeDiff = imageAttach.width() - self.imagePreviewWindow.width()
            imageAttach = imageAttach.scaledToWidth(imageAttach.width()-sizeDiff, mode=Qt.TransformationMode.SmoothTransformation)
        if imageAttach.height() >= self.imagePreviewWindow.height():
            sizeDiff = imageAttach.height() - self.imagePreviewWindow.height()
            imageAttach = imageAttach.scaledToHeight(imageAttach.height()-sizeDiff, mode=Qt.TransformationMode.SmoothTransformation)
  
        self.imagePreviewWidget.setPixmap(
            imageAttach
        )
        self.imagePreviewWidget.mousePressEvent = self.closeImageViewer

    def closeImageViewer(self, event):
        self.imagePreviewWidget.clear()
        self.stackedWidget.setCurrentIndex(StackedWindows.ChatsWindow)
        self.adaptInterface()

    def deleteMsgAttach(self, event): 
        self.replyMsgsList.clear()
        self.attachMenuWidget.hide()
        del self.sendMessageParams['reply_to'] 

    def buildCompactMsgWidget(self, msg: vkapi.Msg):
        messageWidget = MessageWidget()
        messageWidget.msgObject = msg
        messageWidget.avatar.clear()
        messageWidget.text.setText(msg.text.replace('\n',' ')[:24]+'...')
        messageWidget.text.setWordWrap(False)
        messageWidget.name.setText('<b>{} {}</b>'.format(msg.fromId.firstName, msg.fromId.lastName))
        
        messageWidget.imagesWidget.deleteLater()
        messageWidget.replyMsgsWidget.deleteLater()
        messageWidget.date.deleteLater()
        
        messageWidget.avatar.setPixmap(QIcon('data/icons/reply-16-filled.svg').pixmap(QSize(32,32)))
        messageWidget.avatar.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)

        messageWidget.closeAttachButton.setPixmap(QIcon('data/icons/close-16-filled.svg').pixmap(QSize(32,32)))
        messageWidget.closeAttachButton.mousePressEvent = self.deleteMsgAttach

        messageWidget.frame.setStyleSheet('background-color: transparent')

        return messageWidget

    def buildMsgWidget(self, msg: vkapi.Msg):
        messageWidget = MessageWidget()
        messageWidget.msgObject = msg
        messageWidget.avatar.clear()
        messageWidget.avatar.setPixmap(msg.fromId.image)
        messageWidget.text.setText(self.vkapi.improveMsgText(msg.text))
        #messageWidget.text.setMinimumWidth(1)
        messageWidget.date.setText(datetime.fromtimestamp(msg.date).strftime("%H:%M:%S"))
        messageWidget.name.setText('<b>{} {}</b>'.format(msg.fromId.firstName, msg.fromId.lastName))
        messageWidget.messageClicked.connect(self.addReplyMsg)
        
        if len(msg.attachments) == 0:
            messageWidget.imagesWidget.hide()
        else:
            hasImageAttaches = False
            row = 0
            col = 0
            for attach in msg.attachments: 
                if attach.attachType == vkapi.AttachTypes.STICKER:
                    messageWidget.text.clear()
                    messageWidget.text.setPixmap(attach.preview.scaled(128,128, transformMode=Qt.TransformationMode.SmoothTransformation))
                    messageWidget.text.setMinimumSize(128,128)
                    
                if attach.attachType == vkapi.AttachTypes.PHOTO:
                    hasImageAttaches = True
                    image = ClickableAttachWidget()
                    image.setPixmap(attach.preview.scaledToWidth(220, mode=Qt.TransformationMode.SmoothTransformation))
                    image.attachObject = attach
                    image.attachClicked.connect(self.openImageViewer)

                    if col == 2: 
                        col = 0
                        row += 1
                    messageWidget.imagesLayout.addWidget(image, row, col)
                    col += 1

                if attach.attachType == vkapi.AttachTypes.VIDEO:
                    hasImageAttaches = True

                    image = ClickableAttachWidget()
                    image.setPixmap(attach.preview.scaledToWidth(220, mode=Qt.TransformationMode.SmoothTransformation))
                    image.attachObject = attach
                    image.attachClicked.connect(lambda: QtGui.QDesktopServices.openUrl(QUrl(attach.player)))

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
                reply.isReply = True
                reply.replyFrom = messageWidget
                replyWidget = self.buildMsgWidget(reply)
                messageWidget.replyMsgsLayout.addWidget(replyWidget)

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

                chat.text.setText(self.vkapi.improveMsgText(text))
                chat.time.setText(datetime.fromtimestamp(chat.chatObject.previewMsg.date).strftime("%H:%M:%S"))

                if chat.chatObject.unread != 0:
                    chat.unread.setText('<b>'+str(chat.chatObject.unread)+'</b>')
                    chat.unread.setStyleSheet('QLabel { background-color: #99a2ad; color: white; margin: 2}')
                else:
                    chat.unread.clear()
                    chat.unread.setStyleSheet('QLabel { background-color: transparent}')

                self.chatsListLayout.insertWidget(0, chat)
                break

    def replyMsgButtonClicked(self, event): 
        if len(self.replyMsgsList) == 1:
            self.sendMessageParams['reply_to'] = self.replyMsgsList[0].msgObject.id
            self.buildAttachMenu(self.buildCompactMsgWidget(self.replyMsgsList[0].msgObject), vkapi.AttachTypes.REPLY)

            self.replyMsgsList[0].frame.setStyleSheet('background-color: white')
            self.chatMenuStacked.setCurrentIndex(0)
            self.replyMsgsList.clear()

    def addReplyMsg(self, msg: MessageWidget):
        if msg.msgObject.isReply:
            msg = msg.msgObject.replyFrom
        
        if msg not in self.replyMsgsList:
            self.replyMsgsList.append(msg)
            self.selectedMsgsCountLabel.setText('Выделено: '+str(len(self.replyMsgsList)))
            self.chatMenuStacked.setCurrentIndex(1)

            msg.frame.setStyleSheet('background-color: #e4e6e9')
        else:
            del self.replyMsgsList[self.replyMsgsList.index(msg)]
            self.selectedMsgsCountLabel.setText('Выделено: '+str(len(self.replyMsgsList)))

            if len(self.replyMsgsList) == 0:
                self.selectedMsgsCountLabel.clear()
                self.chatMenuStacked.setCurrentIndex(0)

            msg.frame.setStyleSheet('background-color: white')

    def buildAttachMenu(self, attach, attachType: vkapi.AttachTypes):
        self.attachMenuWidget.show()
        while self.attachMenuLayout.count():
            child = self.attachMenuLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if attachType == vkapi.AttachTypes.REPLY:
            self.attachMenuLayout.addWidget(
                attach
            )
    
    def markAsRead(self, chatObject):
        threading.Thread(target=self.vkapi.call, args=('messages.markAsRead',), kwargs={'peer_id':chatObject.id}).start()

        widgets = (self.chatsListLayout.itemAt(i).widget() for i in range(self.chatsListLayout.count())) 
        for chat in widgets:
            if chat.chatObject.id == chatObject.id:
                chat.chatObject.unread = 0
                chat.unread.clear()
                chat.unread.setStyleSheet('QLabel { background-color: transparent}')

    def getHistory(self, msgs, chatObject: vkapi.Chat, count, offset):
        if offset == 0:
            self.activeChatOffset = 0
            while self.msgsListLayout.count():
                child = self.msgsListLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            self.markAsRead(chatObject)

        for msg in msgs:
            messageWidget = self.buildMsgWidget(msg)

            self.msgsListLayout.insertWidget(0, messageWidget)

        self.chatAvatar.setPixmap(chatObject.image.scaled(32,32, transformMode=Qt.TransformationMode.SmoothTransformation))
        self.chatName.setText(chatObject.name[:24])

        if self.scrollArea.verticalScrollBar().value() != self.scrollArea.verticalScrollBar().maximum():
            self.needScrollBottom = False
        else:
            self.needScrollBottom = True

        self.activeChat = chatObject.id
        self.messageTextEdit.setFocus()
        self.adaptInterface()

    def openChat(self, chatObject: vkapi.Chat, count, offset): 
        if offset == 0:
            self.newChatOpened = True
            self.activeChatOffset = 0
            while self.msgsListLayout.count():
                child = self.msgsListLayout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            self.markAsRead(chatObject)       

        self.activeChat = chatObject.id
        self.adaptInterface()
        self.chatAvatar.clear()
        self.chatName.setText('Загрузка')

        if not self.attachMenuWidget.isHidden():
            self.attachMenuWidget.hide()
            self.replyMsgsList.clear()
            del self.sendMessageParams['reply_to']
        if self.chatMenuStacked.currentIndex() == 1:
            self.chatMenuStacked.setCurrentIndex(0)
            self.replyMsgsList.clear()

        args = {
            'peerId':chatObject.id, 'count':count, 'offset':offset,
            '_returnData':[chatObject,count,offset]                 #это надо чтобы getHistory имел данные из аргументов для продолжения
        }

        getHistoryAsync = asyncvkapi.AsyncVKAPI(self.vkapi, "getHistory", **args)
        getHistoryAsync.signals.getHistory.connect(self.getHistory)
        self.threadPool.start(getHistoryAsync)

    def sendMessage(self, text: str, peerId: int, **args):
        if text == '': return
        
        self.needScrollBottom = True
        params = {'message':text,'peer_id':peerId,'random_id':0}
        params.update(args)

        threading.Thread(target=self.vkapi.call, args=("messages.send",), kwargs=params).start()
        
        self.messageTextEdit.clear()
        if not self.attachMenuWidget.isHidden():
            self.attachMenuWidget.hide()
            del self.sendMessageParams['reply_to'] 

    #def scrollAreaResized(self, event):
    #    pass

    def newMsgEvent(self, msg: vkapi.Msg):
        if self.activeChat == msg.peerId:
            messageWidget = self.buildMsgWidget(msg)
            self.msgsListLayout.addWidget(messageWidget)
            
            if self.scrollArea.verticalScrollBar().value() == self.scrollArea.verticalScrollBar().maximum():
                self.needScrollBottom = True
        self.updateChatsList(msg)

    def resizeEvent(self, event):
        if self.width() < self.height():
            self.compactMode = True
        else:
            self.compactMode = False

        if not self.initComplete: return

        self.resizeGuiElements()
        self.adaptInterface()

    def scrollMsgsMoved(self, pos):
        self.lastMsgScrollPosition = pos
        if pos == 0 and self.newChatOpened == False:
            self.activeChatOffset += 20
            self.needOffsetScroll = True
            self.openChat(self.vkapi.chatsCache[self.activeChat], 20, self.activeChatOffset)

        if pos != 0 and pos == self.scrollArea.verticalScrollBar().maximum() and self.newChatOpened == True:
            self.newChatOpened = False

    def scrollMsgsChanged(self):
        if self.needScrollBottom:
            self.scrollArea.verticalScrollBar().setValue(
                self.scrollArea.verticalScrollBar().maximum()
            )
            self.needScrollBottom = False

        if self.needOffsetScroll:
            self.lastMsgScrollPosition = self.scrollArea.verticalScrollBar().maximum() - self.lastMsgScrollMaximum
            self.scrollArea.verticalScrollBar().setValue(self.lastMsgScrollPosition)

            self.needOffsetScroll = False

        self.lastMsgScrollMaximum = self.scrollArea.verticalScrollBar().maximum()
            
    def adaptInterface(self):
        if self.compactMode:
            self.statusBar.hide()
            self.backButtonCompact.show()
            if self.activeChat != 0:
                self.splitter.moveSplitter(0,1)
            else:
                self.splitter.moveSplitter(self.scrollArea_2.width()+self.scrollArea.width(), 1)
        else:
            self.backButtonCompact.hide()
            self.statusBar.show()
            self.splitter.moveSplitter(self.lastSplitterPos,1)

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
        if not self.compactMode:
            self.lastSplitterPos = pos
        self.resizeGuiElements()
    
    def logging(self, text):
        self.statusLogsLabel.setText(text)
        self.statusLogsLabel.setMaximumWidth(self.width())
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()