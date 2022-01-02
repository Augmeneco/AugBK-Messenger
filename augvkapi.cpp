#include "augvkapi.h"
#include <QDebug>

AugVKApi::AugVKApi(){}

AugVKApi::AugVKApi(QString accessToken){
    this->accessToken = accessToken;
    vkapi.setAccessToken(accessToken);
}

void AugVKApi::setAccessToken(QString token){
    accessToken = token;
    vkapi.setAccessToken(accessToken);
}

void AugVKApi::sendMessage(QString text, int peerId, int reply, QStringList attachments){
    QUrlQuery params;
    params.addQueryItem("peer_id", QString::number(peerId));
    params.addQueryItem("random_id","0");
    params.addQueryItem("message", text);

    if (reply != -1)
        params.addQueryItem("reply_to", QString::number(reply));

    if (attachments.count() > 0)
        params.addQueryItem("attachment", attachments.join(","));

    vkapi.call("messages.send", params);
}

void AugVKApi::sendMessage(QString text, int peerId, QStringList attachments){
    sendMessage(text, peerId, -1, attachments);
}

void AugVKApi::sendMessage(QString text, int peerId, int reply){
    sendMessage(text, peerId, reply, QStringList());
}

void AugVKApi::sendMessage(QString text, int peerId){
    sendMessage(text, peerId, -1, QStringList());
}

QList<Msg> AugVKApi::getMsgsById(QList<int> msgsId){
    QList<Msg> result;
    QString ids = "";

    for (int id : msgsId)
        ids += QString::number(id)+",";

    QUrlQuery params;
    params.addQueryItem("message_ids", ids);
    params.addQueryItem("extended", "1");

    QJsonObject response = vkapi.call("messages.getById", params).toObject();

    for (auto jsonEnum : response["items"].toArray()){
        QJsonObject msgObject = jsonEnum.toObject();
        result.append(parseMsg(msgObject));
    }

    return result;
}

Msg AugVKApi::getMsgById(int msgId){
    QList<int> msgsId;
    msgsId.append(msgId);
    return getMsgsById(msgsId).value(0);
}

QList<Msg> AugVKApi::getHistory(int peerId, int count, int offset, int startMessageId){
    QList<Msg> result;

    QUrlQuery params;
    params.addQueryItem("count", QString::number(count));
    params.addQueryItem("offset", QString::number(offset));
    params.addQueryItem("peer_id", QString::number(peerId));
    params.addQueryItem("extended", "1");

    if (startMessageId >= 0)
        params.addQueryItem("start_message_id", QString::number(startMessageId));
    QJsonObject response = vkapi.call("messages.getHistory", params).toObject();

    QList<QString> userTypes = {{"profiles","groups"}};
    for (QString userType : userTypes){
        if (!response.contains(userType)) continue;

        QJsonArray profilesArray = response[userType].toArray();
        for (auto jsonEnum : profilesArray)
            parseUser(jsonEnum.toObject());
    }

    QJsonArray items = response["items"].toArray();
    for (auto jsonEnum : items)
        result.append(parseMsg(jsonEnum.toObject()));

    return result;
}

QList<Msg> AugVKApi::getHistory(int peerId, int count, int offset){
    return getHistory(peerId, count, offset, -1);
}

QList<Msg> AugVKApi::getHistory(int peerId, int count){
    return getHistory(peerId, count, 0, -1);
}

QString AugVKApi::getPhotoUrl(QJsonArray data, int neededSize){ //затычка, переделать
    QString result;

    QJsonObject resultObject = data[data.count()-1].toObject();

    if (resultObject.contains("url"))
        result = resultObject["url"].toString();
    else
        result = resultObject["src"].toString();

    return result;
}

void AugVKApi::getLPMsg(Msg msg){
    qDebug() << "New Msg: " << msg.text;
}

Msg AugVKApi::parseLpMsg(QJsonArray data){
    Msg result;
    result.id = data[1].toInt();
    result.date = -1;

    if (!data[6].toObject().contains("from")){
        result = getMsgById(data[1].toInt()); //почему то в старом апи написано что это костыль и надо фиксить
        return result;
    }

    result.fromId = getUser(data[6].toObject()["from"].toString().toInt());
    result.peerId = data[3].toInt();
    result.text = data[5].toString();

    return result;
}

Msg AugVKApi::parseMsg(QJsonObject data){
    Msg result;
    result.id = data["id"].toInt();
    result.text = data["text"].toString();
    result.fromId = getUser(data["from_id"].toInt());
    result.peerId = data["peer_id"].toInt();
    result.date = data["date"].toInt();

    if (data["attachments"].toArray().count() != -1){
        for (auto jsonEnum : data["attachments"].toArray()){
            QJsonObject attachmentsObj = jsonEnum.toObject();

            if (attachmentsObj["type"].toString() == "sticker"){
                Attachment attachment;
                QJsonArray sizes = attachmentsObj["sticker"].toObject()["images_with_background"].toArray();
                attachment.url = sizes[sizes.count()-1].toObject()["url"].toString();
                attachment.name = "Sticker"+attachmentsObj["sticker"].toObject()["sticker_id"].toString();
                //attachment.preview = loadPhoto(attachment.url); todo
                attachment.attachType = attachTypes::STICKER;

                result.attachments.append(attachment);
            }
        }
    }

    return result;
}

User AugVKApi::getUser(int id){
    QList<int> users;
    users.append(id);
    return getUsers(users).value(0);
}

QList<User> AugVKApi::getUsers(QList<int> ids){
    QString userIds = "";
    QList<User> result;

    bool exists;
    for (int id : ids){
        //todo: затычка от краша на ботах, последствия НЕ ИЗВЕСТНЫ, бот может даже не появиться в кэше, но вопрос как он попал сюда?
        if (id < 0) continue;

        exists = false;
        for (User user : usersCache){
            if (user.id == id){
                result.append(user);
                exists = true;
                break;
            }
        }
        if (!exists)
            userIds += QString::number(id)+",";
    }

    if (userIds != ""){
        QUrlQuery params;
        params.addQueryItem("fields","photo_50, last_seen");

        if (userIds != "-1,")
            params.addQueryItem("user_ids", userIds);

        QJsonArray response = vkapi.call("users.get", params).toArray();
        for (auto jsonEnum : response){
            QJsonObject userObject = jsonEnum.toObject();
            result.append(parseUser(userObject));
        }
    }
    return result;
}

void AugVKApi::addUser(User user){
    for (User i : usersCache)
        if (i.id == user.id) return;
    usersCache.append(user);
}

User AugVKApi::parseGroup(QJsonObject data){
    if ((data["type"].toString() == "group") || (data["type"].toString() == "page")){
        User result;
        result.id = data["id"].toInt() * -1;
        result.firstName = "";
        //todo
        //result.image = loadPhoto(data["photo_50"].toString());

        addUser(result);
        return result;
    }else{
        throw VKException("Объект не группы не должен тут появляться");
    }
}

User AugVKApi::parseUser(QJsonObject data){
    User result;
    result.id = data["id"].toInt();

    for (User user : usersCache)
        if (user.id == data["id"].toInt()){
            result = user;
            return result;
        }

    if (data.contains("type"))
        if ((data["type"].toString() == "group") ||
            (data["type"].toString() == "page")  ||
             data["id"].toInt() < 0){

            result = parseGroup(data);
            return result;
        }

    result.firstName = data["first_name"].toString();
    result.lastName = data["last_name"].toString();

    //todo
    //result.image = loadPhoto(data["photo_50"].toString());
    addUser(result);
    return result;
}

QList<Chat> AugVKApi::getConversations(int count, int offset){
    QList<Chat> result;
    if (count > 200) count = 200;

    QUrlQuery params;
    params.addQueryItem("offset", QString::number(offset));
    params.addQueryItem("count", QString::number(count));
    params.addQueryItem("extended","1");

    QJsonObject response = vkapi.call("messages.getConversations", params).toObject();
    QJsonArray chatsArray = response["items"].toArray();
    if (chatsArray.count() == 0) return result;

    qDebug() << QString("Loading chats %1 / %2").arg(
                    QString::number(offset),
                    QString::number(response["count"].toInt()) );

    QList<QString> userTypes = {{"profiles","groups"}};
    for (QString userType : userTypes){
        if (!response.contains(userType)) continue;

        QJsonArray profilesArray = response[userType].toArray();
        for (auto jsonEnum : profilesArray){
            parseUser(jsonEnum.toObject());
        }
    }

    for (auto jsonEnum : chatsArray){
        QJsonObject chatObject = jsonEnum.toObject();

        int chatId = chatObject["conversation"].toObject()["peer"].toObject()["id"].toInt();
        if (chatsCache.contains(chatId)){
            result.append(chatsCache.value(chatId));
            continue;
        }

        Chat resultVar;
        resultVar.id = chatObject["conversation"].toObject()["peer"].toObject()["id"].toInt();
        resultVar.previewMsg = parseMsg(chatObject["last_message"].toObject());

        if (chatObject["conversation"].toObject()["peer"].toObject()["type"].toString() == "chat"){
            resultVar.name = chatObject["conversation"].toObject()["chat_settings"].toObject()["title"].toString();

            if (!chatObject["conversation"].toObject()["chat_settings"].toObject().contains("photo")){
                resultVar.image = resultVar.previewMsg.fromId.image;
            }else{
                //todo
                //resultVar.image = loadPhoto(
                //            chatObject["conversation"].toObject()["chat_settings"].toObject()["photo"].toObject()["photo_50"].toString());
            }
        }else{
            User user = getUser(resultVar.id);
            resultVar.name = user.firstName + " " + user.lastName;
            resultVar.image = user.image;
        }
        result.append(resultVar);
        chatsCache[resultVar.id] = resultVar;
    }

    return result;
}
