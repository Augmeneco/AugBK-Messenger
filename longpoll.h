#ifndef LONGPOLL_H
#define LONGPOLL_H

#include <QObject>
#include "vkapi.h"
#include "requests.h"
#include "augvkapi.h"

class LongPoll: public QObject
{
    Q_OBJECT
public:
    LongPoll();
    LongPoll(QString accessToken);
    void start();

private:
    void updateLP();
    VKAPI vkapi;
    Requests requests;

    QString LPServer;
    QString LPKey;
    int LPTS;

signals:
    void newMsg(Msg response);
};

#endif // LONGPOLL_H
