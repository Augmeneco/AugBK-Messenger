#include "requests.h"

Requests::Requests(QObject *parentForm){
    this->networkManager = new QNetworkAccessManager(parentForm);
}

Requests::Requests(){
    this->networkManager = new QNetworkAccessManager(nullptr);
}

Requests::~Requests(){
    delete networkManager;
}

void Requests::addHeaders(QString key, QString value){
    this->headers[key] = value;
}

RequestsResponse Requests::post(QString urlString){
    return post(urlString, QUrlQuery());
}

RequestsResponse Requests::post(QString urlString, QUrlQuery params){
    QEventLoop event;

    QUrl url = QUrl(urlString);

    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader,QVariant("application/x-www-form-urlencoded"));
    if (this->headers.count() > 0){
        for (auto i : this->headers.toStdMap()){
            request.setRawHeader(i.first.toLocal8Bit(), i.second.toLocal8Bit());
        }
    }

    QNetworkReply *reply = this->networkManager->post(request, params.toString(QUrl::FullyEncoded).toUtf8());
    QObject::connect(reply,SIGNAL(finished()), &event, SLOT(quit()));
    event.exec();

    RequestsResponse response;
    response.text = reply->readAll();

    delete reply;

    return response;
}

RequestsResponse Requests::get(QString urlString){
    return get(urlString, QUrlQuery());
}

RequestsResponse Requests::get(QString urlString, QUrlQuery params){
    QEventLoop event;

    QUrl url = QUrl(urlString);

    if (!params.isEmpty())
        url.setQuery(params);

    QNetworkRequest request(url);
    if (this->headers.count() > 0){
        for (auto i : this->headers.toStdMap()){
            request.setRawHeader(i.first.toLocal8Bit(), i.second.toLocal8Bit());
        }
    }

    QNetworkReply *reply = this->networkManager->get(request);
    QObject::connect(reply,SIGNAL(finished()), &event, SLOT(quit()));
    event.exec();

    RequestsResponse response;
    response.text = reply->readAll();

    delete reply;

    return response;
}

QJsonDocument RequestsResponse::json(){
    return QJsonDocument::fromJson(
                this->text.toUtf8()
    );
}
