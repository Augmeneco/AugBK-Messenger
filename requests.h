#ifndef REQUESTS_H
#define REQUESTS_H

#include <QJsonObject>
#include <QJsonArray>
#include <QJsonDocument>
#include <QtNetwork/QtNetwork>
#include <QUrl>
#include <QUrlQuery>
#include <QMap>

class RequestsResponse
{
public:
    QString text;
    QJsonDocument json();
};

class Requests
{
public:
    Requests(QObject *parentForm);
    Requests();
    ~Requests();
    RequestsResponse get(QString urlString, QUrlQuery params);
    RequestsResponse get(QString urlString);
    RequestsResponse post(QString urlString, QUrlQuery params);
    RequestsResponse post(QString urlString);
    void addHeaders(QString key, QString value);

private:
    QNetworkAccessManager *networkManager;
    QMap<QString, QString> headers;
};

#endif // REQUESTS_H
