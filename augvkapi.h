#ifndef AUGVKAPI_H
#define AUGVKAPI_H

#include <QObject>
#include <QDebug>
#include <QList>
#include <QImage>
#include "requests.h"
#include "vkapi.h"

enum attachTypes{PHOTO,VIDEO,AUDIO,DOC,WALL,MARKET,POLL,STICKER,GIF,URL};
enum photoSizes{SMALL,MEDIUM,BIG};

class Attachment
{
public:
    //~Attachment(); todo

    QString name;
    QString url;
    QImage preview;
    attachTypes attachType;
};

class User
{
public:
    QString firstName;
    QString lastName;
    int id;
    QImage image;
};

class Msg
{
public:
    int id;
    QString text;
    int date;
    int peerId;
    User fromId;
    QList<Msg> reply;
    QList<Attachment> attachments;
};

class Chat
{
public:
    int id;
    QString name;
    Msg previewMsg;
    QImage image;
    QString type; //"Form" in legacy pascal api
};

class AugVKApi : public QObject
{
    Q_OBJECT
public:
    AugVKApi();
    AugVKApi(QString accessToken);

    void setAccessToken(QString token);

    QList<Chat> getConversations(int count, int offset=0);
    Chat getConversationById(int id);

    User parseUser(QJsonObject data);
    User parseGroup(QJsonObject data);
    Msg parseMsg(QJsonObject data);
    Msg parseLpMsg(QJsonArray data);

    Msg getMsgById(int msgId);
    QList<Msg> getMsgsById(QList<int> msgsId);

    void addUser(User user);
    User getUser(int id);
    QList<User> getUsers(QList<int> ids);

    QList<Msg> getHistory(int peerId, int count, int offset, int startMessageId);
    QList<Msg> getHistory(int peerId, int count, int offset);
    QList<Msg> getHistory(int peerId, int count);

    QString getPhotoUrl(QJsonArray data, int neededSize=photoSizes::BIG);
    QString getAttachmentName(QJsonObject attachObject);

    void sendMessage(QString text, int peerId, int reply, QStringList attachments);
    void sendMessage(QString text, int peerId, QStringList attachments);
    void sendMessage(QString text, int peerId, int reply);
    void sendMessage(QString text, int peerId);

public slots:
    void getLPMsg(Msg msg);

private:
    QString accessToken;
    VKAPI vkapi;

    Requests requests;
    QList<User> usersCache;
    QMap<int,Chat> chatsCache;
};

#endif // AUGVKAPI_H
