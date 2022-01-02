QT       += core gui network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    chatwidget.cpp \
    main.cpp \
    mainwindow.cpp \
    messagewidget.cpp \
    augvkapi.cpp \
    longpoll.cpp \
    vkapi.cpp \
    requests.cpp

HEADERS += \
    chatwidget.h \
    mainwindow.h \
    messagewidget.h \
    augvkapi.h \
    longpoll.h \
    vkapi.h \
    requests.h

FORMS += \
    chatwidget.ui \
    mainwindow.ui \
    messagewidget.ui

TRANSLATIONS += \
    AugBK-Messenger_ru_RU.ts
CONFIG += lrelease
CONFIG += embed_translations

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    main.qrc


