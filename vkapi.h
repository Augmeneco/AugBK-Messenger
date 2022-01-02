#ifndef VKAPI_H
#define VKAPI_H

#include <QJsonObject>
#include <QJsonArray>
#include <QJsonDocument>
#include <QObject>
#include <QDebug>
#include "requests.h"
#include <exception>

class VKAPI : public QObject
{
    Q_OBJECT
public:
    VKAPI();
    VKAPI(QString accessToken);

    QJsonValue call(QString method, QUrlQuery params);

    void setAccessToken(QString token){ accessToken = token; }
private:
    QString accessToken;
    Requests requests;
    QString apiVersion = "5.131";
};

class VKException: public std::runtime_error
{
public:
    VKException(const char *msg) : runtime_error(msg) {};
    VKException() throw();
};

#endif // VKAPI_H
