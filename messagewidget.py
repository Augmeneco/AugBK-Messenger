# Form implementation generated from reading ui file '.\messagewidget.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(294, 85)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.avatar = QtWidgets.QLabel(Form)
        self.avatar.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.avatar.setObjectName("avatar")
        self.verticalLayout_2.addWidget(self.avatar)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("QFrame#frame {\n"
"background-color: white; }")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.name = QtWidgets.QLabel(self.frame)
        self.name.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.name.setWordWrap(False)
        self.name.setObjectName("name")
        self.horizontalLayout_3.addWidget(self.name)
        self.date = QtWidgets.QLabel(self.frame)
        self.date.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.date.setWordWrap(False)
        self.date.setObjectName("date")
        self.horizontalLayout_3.addWidget(self.date)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.imagesWidget = QtWidgets.QWidget(self.frame)
        self.imagesWidget.setObjectName("imagesWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.imagesWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.imagesLayout = QtWidgets.QGridLayout()
        self.imagesLayout.setObjectName("imagesLayout")
        self.verticalLayout_3.addLayout(self.imagesLayout)
        self.verticalLayout.addWidget(self.imagesWidget)
        self.replyMsgsWidget = QtWidgets.QWidget(self.frame)
        self.replyMsgsWidget.setObjectName("replyMsgsWidget")
        self.replyMsgs = QtWidgets.QHBoxLayout(self.replyMsgsWidget)
        self.replyMsgs.setContentsMargins(0, 0, 0, 0)
        self.replyMsgs.setObjectName("replyMsgs")
        self.line = QtWidgets.QFrame(self.replyMsgsWidget)
        self.line.setStyleSheet("background-color: rgb(170, 188, 206);")
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.replyMsgs.addWidget(self.line)
        self.replyMsgsLayout = QtWidgets.QVBoxLayout()
        self.replyMsgsLayout.setObjectName("replyMsgsLayout")
        self.replyMsgs.addLayout(self.replyMsgsLayout)
        self.verticalLayout.addWidget(self.replyMsgsWidget)
        self.textLayout = QtWidgets.QHBoxLayout()
        self.textLayout.setSpacing(6)
        self.textLayout.setObjectName("textLayout")
        self.text = QtWidgets.QLabel(self.frame)
        self.text.setStyleSheet("")
        self.text.setScaledContents(False)
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft)
        self.text.setWordWrap(True)
        self.text.setObjectName("text")
        self.textLayout.addWidget(self.text)
        self.verticalLayout.addLayout(self.textLayout)
        self.verticalLayout.setStretch(3, 1)
        self.horizontalLayout.addWidget(self.frame)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.closeAttachButton = QtWidgets.QLabel(Form)
        self.closeAttachButton.setText("")
        self.closeAttachButton.setObjectName("closeAttachButton")
        self.horizontalLayout_2.addWidget(self.closeAttachButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.avatar.setText(_translate("Form", "avatar"))
        self.name.setText(_translate("Form", "name"))
        self.date.setText(_translate("Form", "date"))
        self.text.setText(_translate("Form", "text"))
