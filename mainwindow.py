# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(814, 548)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.mainPage = QtWidgets.QWidget()
        self.mainPage.setObjectName("mainPage")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.mainPage)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter = QtWidgets.QSplitter(self.mainPage)
        self.splitter.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.splitter.setLineWidth(10)
        self.splitter.setMidLineWidth(5)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.menuButton = QtWidgets.QPushButton(self.layoutWidget)
        self.menuButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.menuButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("data/icons/navigation-16-filled.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menuButton.setIcon(icon)
        self.menuButton.setIconSize(QtCore.QSize(32, 32))
        self.menuButton.setFlat(True)
        self.menuButton.setObjectName("menuButton")
        self.horizontalLayout_2.addWidget(self.menuButton)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.layoutWidget)
        self.scrollArea_2.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 223, 476))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.chatsListWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.chatsListWidget.setObjectName("chatsListWidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.chatsListWidget)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.chatsListLayout = QtWidgets.QVBoxLayout()
        self.chatsListLayout.setObjectName("chatsListLayout")
        self.verticalLayout_8.addLayout(self.chatsListLayout)
        self.verticalLayout_5.addWidget(self.chatsListWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea_2)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chatMenuStacked = QtWidgets.QStackedWidget(self.layoutWidget1)
        self.chatMenuStacked.setObjectName("chatMenuStacked")
        self.chatInfoPage = QtWidgets.QWidget()
        self.chatInfoPage.setObjectName("chatInfoPage")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.chatInfoPage)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.backButtonCompact = QtWidgets.QPushButton(self.chatInfoPage)
        self.backButtonCompact.setMinimumSize(QtCore.QSize(0, 0))
        self.backButtonCompact.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        self.backButtonCompact.setFont(font)
        self.backButtonCompact.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("data/icons/arrow-left-16-filled.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.backButtonCompact.setIcon(icon1)
        self.backButtonCompact.setIconSize(QtCore.QSize(32, 32))
        self.backButtonCompact.setFlat(True)
        self.backButtonCompact.setObjectName("backButtonCompact")
        self.horizontalLayout_4.addWidget(self.backButtonCompact)
        self.chatAvatar = QtWidgets.QLabel(self.chatInfoPage)
        self.chatAvatar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.chatAvatar.setText("")
        self.chatAvatar.setObjectName("chatAvatar")
        self.horizontalLayout_4.addWidget(self.chatAvatar)
        self.chatName = QtWidgets.QLabel(self.chatInfoPage)
        self.chatName.setStyleSheet("margin-left: 6")
        self.chatName.setText("")
        self.chatName.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.chatName.setWordWrap(True)
        self.chatName.setObjectName("chatName")
        self.horizontalLayout_4.addWidget(self.chatName)
        self.chatInfoButton = QtWidgets.QPushButton(self.chatInfoPage)
        self.chatInfoButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.chatInfoButton.setText("")
        self.chatInfoButton.setIcon(icon)
        self.chatInfoButton.setIconSize(QtCore.QSize(32, 32))
        self.chatInfoButton.setFlat(True)
        self.chatInfoButton.setObjectName("chatInfoButton")
        self.horizontalLayout_4.addWidget(self.chatInfoButton)
        self.horizontalLayout_4.setStretch(2, 1)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.chatMenuStacked.addWidget(self.chatInfoPage)
        self.selectedMsgPage = QtWidgets.QWidget()
        self.selectedMsgPage.setObjectName("selectedMsgPage")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.selectedMsgPage)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(5, -1, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.selectedMsgsCountLabel = QtWidgets.QLabel(self.selectedMsgPage)
        self.selectedMsgsCountLabel.setObjectName("selectedMsgsCountLabel")
        self.horizontalLayout_6.addWidget(self.selectedMsgsCountLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.replyMsgButton = QtWidgets.QPushButton(self.selectedMsgPage)
        self.replyMsgButton.setObjectName("replyMsgButton")
        self.horizontalLayout_6.addWidget(self.replyMsgButton)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        self.chatMenuStacked.addWidget(self.selectedMsgPage)
        self.verticalLayout_3.addWidget(self.chatMenuStacked)
        self.scrollArea = QtWidgets.QScrollArea(self.layoutWidget1)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 575, 235))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.msgsListWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.msgsListWidget.setObjectName("msgsListWidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.msgsListWidget)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.msgsListLayout = QtWidgets.QVBoxLayout()
        self.msgsListLayout.setSpacing(6)
        self.msgsListLayout.setObjectName("msgsListLayout")
        self.verticalLayout_7.addLayout(self.msgsListLayout)
        self.verticalLayout_6.addWidget(self.msgsListWidget)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.attachMenuWidget = QtWidgets.QWidget(self.layoutWidget1)
        self.attachMenuWidget.setEnabled(True)
        self.attachMenuWidget.setObjectName("attachMenuWidget")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.attachMenuWidget)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.attachMenuLayout = QtWidgets.QHBoxLayout()
        self.attachMenuLayout.setObjectName("attachMenuLayout")
        self.verticalLayout_11.addLayout(self.attachMenuLayout)
        self.verticalLayout_3.addWidget(self.attachMenuWidget)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.attachButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.attachButton.setMinimumSize(QtCore.QSize(0, 0))
        self.attachButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("data/icons/attach-16-filled.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.attachButton.setIcon(icon2)
        self.attachButton.setIconSize(QtCore.QSize(32, 32))
        self.attachButton.setFlat(True)
        self.attachButton.setObjectName("attachButton")
        self.horizontalLayout_5.addWidget(self.attachButton)
        self.messageTextEdit = QtWidgets.QPlainTextEdit(self.layoutWidget1)
        self.messageTextEdit.setMaximumSize(QtCore.QSize(16777215, 40))
        self.messageTextEdit.setUndoRedoEnabled(True)
        self.messageTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.messageTextEdit.setPlainText("")
        self.messageTextEdit.setObjectName("messageTextEdit")
        self.horizontalLayout_5.addWidget(self.messageTextEdit)
        self.sendMessageButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.sendMessageButton.setMinimumSize(QtCore.QSize(0, 0))
        self.sendMessageButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("data/icons/send-16-filled.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.sendMessageButton.setIcon(icon3)
        self.sendMessageButton.setIconSize(QtCore.QSize(32, 32))
        self.sendMessageButton.setAutoExclusive(False)
        self.sendMessageButton.setFlat(True)
        self.sendMessageButton.setObjectName("sendMessageButton")
        self.horizontalLayout_5.addWidget(self.sendMessageButton)
        self.emojiButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.emojiButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("data/icons/emoji-16-regular.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.emojiButton.setIcon(icon4)
        self.emojiButton.setIconSize(QtCore.QSize(32, 32))
        self.emojiButton.setFlat(True)
        self.emojiButton.setObjectName("emojiButton")
        self.horizontalLayout_5.addWidget(self.emojiButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(3, 1)
        self.verticalLayout_4.addWidget(self.splitter)
        self.stackedWidget.addWidget(self.mainPage)
        self.authByWebEngine = QtWidgets.QWidget()
        self.authByWebEngine.setObjectName("authByWebEngine")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.authByWebEngine)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.authByTokenButton2 = QtWidgets.QPushButton(self.authByWebEngine)
        self.authByTokenButton2.setObjectName("authByTokenButton2")
        self.horizontalLayout_8.addWidget(self.authByTokenButton2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.verticalLayout_12.addLayout(self.horizontalLayout_8)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.authByWebEngine)
        self.webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.webEngineView.setObjectName("webEngineView")
        self.verticalLayout_12.addWidget(self.webEngineView)
        self.verticalLayout_12.setStretch(1, 1)
        self.stackedWidget.addWidget(self.authByWebEngine)
        self.authByTokenWindow = QtWidgets.QWidget()
        self.authByTokenWindow.setObjectName("authByTokenWindow")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.authByTokenWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.authByTokenWindow)
        self.label.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.authByTokenEdit = QtWidgets.QLineEdit(self.authByTokenWindow)
        self.authByTokenEdit.setObjectName("authByTokenEdit")
        self.verticalLayout.addWidget(self.authByTokenEdit)
        self.authByTokenButton = QtWidgets.QPushButton(self.authByTokenWindow)
        self.authByTokenButton.setObjectName("authByTokenButton")
        self.verticalLayout.addWidget(self.authByTokenButton)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.stackedWidget.addWidget(self.authByTokenWindow)
        self.imagePreviewWindow = QtWidgets.QWidget()
        self.imagePreviewWindow.setObjectName("imagePreviewWindow")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.imagePreviewWindow)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.imagePreviewWidget = QtWidgets.QLabel(self.imagePreviewWindow)
        self.imagePreviewWidget.setText("")
        self.imagePreviewWidget.setScaledContents(False)
        self.imagePreviewWidget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.imagePreviewWidget.setObjectName("imagePreviewWidget")
        self.verticalLayout_9.addWidget(self.imagePreviewWidget)
        self.stackedWidget.addWidget(self.imagePreviewWindow)
        self.verticalLayout_10.addWidget(self.stackedWidget)
        self.statusBar = QtWidgets.QWidget(self.centralwidget)
        self.statusBar.setObjectName("statusBar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.statusBar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.statusLogsLabel = QtWidgets.QLabel(self.statusBar)
        self.statusLogsLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.statusLogsLabel.setWordWrap(False)
        self.statusLogsLabel.setObjectName("statusLogsLabel")
        self.horizontalLayout.addWidget(self.statusLogsLabel)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout_10.addWidget(self.statusBar)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.selectedMsgsCountLabel.setText(_translate("MainWindow", "selectedMsgsCount"))
        self.replyMsgButton.setText(_translate("MainWindow", "Ответить"))
        self.authByTokenButton2.setText(_translate("MainWindow", "Авторизация через токен"))
        self.label.setText(_translate("MainWindow", "<a href=\"https://oauth.vk.com/oauth/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1&slogin_h=313cdef0b2177ec401.351765a09fcd1f2bba&__q_hash=908b8d205940c31676e11f938782deb7\">Получить токен Kate Mobile</a>"))
        self.authByTokenEdit.setPlaceholderText(_translate("MainWindow", "Вставьте ссылку с токеном"))
        self.authByTokenButton.setText(_translate("MainWindow", "Войти"))
        self.statusLogsLabel.setText(_translate("MainWindow", "Debug"))
from PyQt6 import QtWebEngineWidgets
