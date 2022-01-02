#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QResizeEvent>

enum MainWindowState {
    ConversationsAndChat,
    OnlyConversations,
    OnlyChat
};

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

private:
    Ui::MainWindow *ui;
    MainWindowState windowState;

    void resizeEvent(QResizeEvent*);

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    MainWindowState getWindowState() const;
    void setWindowState(MainWindowState newWindowState);
private slots:
    void on_pushButton_clicked();
};
#endif // MAINWINDOW_H
