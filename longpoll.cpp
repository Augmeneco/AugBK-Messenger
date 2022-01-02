#include "longpoll.h"
#include "augvkapi.h"

AugVKApi augvkapi;

LongPoll::LongPoll(QString accessToken){
    vkapi.setAccessToken(accessToken);
    augvkapi.setAccessToken(accessToken);
}

LongPoll::LongPoll(){}

void LongPoll::updateLP(){
    QUrlQuery params;
    params.addQueryItem("lp_version","3");

    QJsonObject LPData = vkapi.call("messages.getLongPollServer", params).toObject();

    LPServer = LPData["server"].toString();
    LPKey = LPData["key"].toString();
    LPTS = LPData["ts"].toInt();

    qDebug() << "New longpoll info received";
}

void LongPoll::start(){
    updateLP();

    while (true){
        QJsonObject LPResponse = requests.get(
            QString("https://%1?act=a_check&key=%2&ts=%3&wait=25&mode=2&version=3").arg(
                LPServer,
                LPKey,
                QString::number(LPTS)
            )
        ).json().object();

        if (LPResponse.contains("failed")){
           int failedNum = LPResponse["failed"].toInt();

           if (failedNum == 1){
               LPTS = LPResponse["ts"].toInt();
               continue;
           }
           if ((failedNum == 2) || (failedNum == 3)){
               updateLP();
               continue;
           }
        }
        LPTS = LPResponse["ts"].toInt();
        for (auto v : LPResponse["updates"].toArray()){
            QJsonArray event = v.toArray();

            if (event[0].toInt() != 4) continue;

            Msg msg = augvkapi.getMsgById(event[1].toInt()); //либо юзать augvkapi.parseLpMsg(event) если не надо трогать апи вк

            emit newMsg(msg);
        }
    }
}
