#include "vkapi.h"

VKAPI::VKAPI(QString accessToken){
    this->accessToken = accessToken;
}

VKAPI::VKAPI(){}

QJsonValue VKAPI::call(QString method, QUrlQuery params){
    qDebug() << "Call " << method;
    params.addQueryItem("v",apiVersion);
    params.addQueryItem("access_token",accessToken);

    QJsonDocument response = requests.post(
        QString("https://api.vk.com/method/%1").arg(method),
        params
    ).json();

    if (response.object().contains("error")){
        if (response["error"].toObject()["error_code"].toInt() == 6){
            //костылище какое-то ради слипа обычного

            QTime dieTime = QTime::currentTime().addSecs(1);
            while (QTime::currentTime() < dieTime)
                QCoreApplication::processEvents(QEventLoop::AllEvents, 100);
            qDebug() << "Forced sleep";

            return call(method, params);

        }

        qDebug() << response;

        throw VKException(
            QString("VK ERROR #%1: \"%2\"\nParams: %3").arg(
                QString::number(response.object()["error"].toObject()["error_code"].toInt()),
                response.object()["error"].toObject()["error_msg"].toString(),
                QString(QJsonDocument(response.object()["error"].toObject()["request_params"].toArray()).toJson())
            ).toLocal8Bit()
        );
    }

    return response.object()["response"];
}
