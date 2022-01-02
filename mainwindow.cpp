#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "chatwidget.h"
#include "messagewidget.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->layoutChatList->addWidget(new ChatWidget(this));
    ui->layoutMessagesList->addWidget(new MessageWidget(this));
}

MainWindow::~MainWindow()
{
    delete ui;
}

MainWindowState MainWindow::getWindowState() const
{
    return windowState;
}

void MainWindow::setWindowState(MainWindowState newWindowState)
{
    windowState = newWindowState;

    switch (newWindowState) {
        case ConversationsAndChat:
            ui->conversationsArea->show();
            ui->chatArea->show();
            ui->returnButton->hide();
        break;
        case OnlyConversations:
            ui->conversationsArea->show();
            ui->chatArea->hide();
        break;
        case OnlyChat:
            ui->conversationsArea->hide();
            ui->chatArea->show();
            ui->returnButton->show();
        break;
    }
}

void MainWindow::resizeEvent(QResizeEvent* event)
{
   QMainWindow::resizeEvent(event);

   if (event->size().width() < 550) {
       setWindowState(OnlyConversations);
   } else {
      setWindowState(ConversationsAndChat);
   }

   ui->statusbar->showMessage(QString::number(event->size().width())+" "+QString::number(ui->conversationsArea->width())+" "+QString::number(ui->chatArea->width()));
}

void MainWindow::on_pushButton_clicked()
{
    setWindowState(OnlyConversations);
}

