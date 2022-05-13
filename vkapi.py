from enum import Enum
from PyQt6 import QtCore, QtNetwork, QtGui

import requests, os, time

class AttachTypes(Enum):
    PHOTO = 1
    VIDEO = 2
    AUDIO = 3
    DOC = 4
    WALL= 5
    STICKER = 6 
    THUMBNAIL = 7
    GIF = 8

class PhotoSize(Enum):
    SMALL = 1
    MEDIUM = 2
    BIG = 3

class Attachment:
    name: str
    url: str
    preview: bytes
    attachType: AttachTypes

class User:
    firstName: str
    lastName: str
    id: int
    image: QtGui.QPixmap

class Msg:
    id: int
    text: str
    date: int
    fromId: User
    peerId: int
    reply: list
    attachments: list
    deleted = False

class Chat:
    id: int
    name: str
    previewMsg: Msg
    image: QtGui.QPixmap
    type: str
    unread: int


class VK_API(QtCore.QObject):
    def __init__(self, access_token):
        QtCore.QObject.__init__(self)

        self.access_token = access_token
        self.version = 5.131
        self.usersCache = []
        self.chatsCache = {}

    def call(self, method, **parameters):
        print('Call method '+method)
        url = 'https://api.vk.com/method/' + method
        parameters['access_token'] = self.access_token
        if 'v' not in parameters:
            parameters['v'] = self.version

        result = requests.post(url, params=parameters).json()

        if 'error' in result:
            if result['error']['error_code'] == 6 or result['error']['error_code'] == 10:
                time.sleep(2)
                print('Forced sleep')
                return self.call(method, **parameters)


            error_string = 'VK ERROR #{}: "{}"\nPARAMS: {}'.format(result['error']['error_code'],
                                                        result['error']['error_msg'],
                                                        result['error']['request_params'])
            print(error_string)
            raise Exception(error_string)

        return result['response']

    def getAttachmentName(self, data):
        attachType = data['type']

        return attachType + str(data[attachType]['owner_id']) +'_'+ str(data[attachType]['id'])

    def loadAttach(self, name, fileType: AttachTypes, url) -> QtGui.QPixmap:
        path = ''
        name = str(name)
        if fileType == AttachTypes.PHOTO:
            path += 'photos/'+name+'.jpg'
        if fileType == AttachTypes.STICKER:
            path += 'stickers/'+name+'.png'
        if fileType == AttachTypes.THUMBNAIL:
            path += 'thumbnails/'+name+'.png'
        
        return self.loadPhoto(url, path)

    def loadPhoto(self, url, path) -> QtGui.QPixmap:
        print('Loading photo '+path)
        pixMap = QtGui.QPixmap()

        dirPath = '/'.join(('data/images/'+path).split('/')[:-1])
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        if not os.path.exists('data/images/'+path):
            response = requests.get(url)
            file = open('data/images/'+path,'wb')
            file.write(response.content)
            file.close()

        pixMap.load('data/images/'+path)
        return pixMap
        


    def getPhotoUrl(self, data, neededSize=PhotoSize.MEDIUM): #затычка, переделать как в паскале #todo
        result = ''

        resultObject = data[-1]
        if 'url' in resultObject:
            result = resultObject['url']
        else:
            result = resultObject['src']

        return result

    def getChats(self, count, offset = 0):
        result = []
        if count > 200: count = 200

        response = self.call('messages.getConversations',
            offset=offset, count=count, extended=1
        )
        print('Loading chats {}/{}'.format(offset, response['count']))

        chats = response['items']
        if len(chats) == 0: return result

        for userType in ['profiles','groups']:
            if userType not in response: continue

            profiles = response[userType]
            for profile in profiles:
                self.parseUser(profile)

        users = []
        for chat in chats:
            if chat['last_message']['from_id'] > 0:
                users.append(chat['last_message']['from_id'])
            if chat['conversation']['peer']['type'] == 'user': 
                users.append(chat['conversation']['peer']['id'])

        self.getUsers(users)

        for chat in chats:
            if chat['conversation']['peer']['id'] in self.chatsCache:
                result.append(self.chatsCache[chat['conversation']['peer']['id']])
                continue

            resultVar = Chat()
            resultVar.id = chat['conversation']['peer']['id']
            resultVar.previewMsg = self.parseMsg(chat['last_message'])
            
            if 'unread_count' in chat['conversation']:
                resultVar.unread = chat['conversation']['unread_count']
            else:
                resultVar.unread = 0

            if chat['conversation']['peer']['type'] == 'chat':
                resultVar.name = chat['conversation']['chat_settings']['title']

                if 'photo' not in chat['conversation']['chat_settings']:
                    resultVar.image = resultVar.previewMsg.fromId.image
                else:
                    resultVar.image = self.loadAttach(
                        resultVar.id,
                        AttachTypes.PHOTO,
                        chat['conversation']['chat_settings']['photo']['photo_50']
                    )
            else:
                user = self.getUser(resultVar.id)
                resultVar.name = user.firstName +' '+ user.lastName
                resultVar.image = user.image
            result.append(resultVar)
            self.chatsCache[resultVar.id] = resultVar

        return result

    def getHistory(self, peerId, count, offset=0, startMessageId=-1):
        result = []

        params = {}
        params['count'] = count
        params['offset'] = offset
        params['peer_id'] = peerId
        params['extended'] = 1

        if startMessageId >= 0:
            params['start_message_id'] = startMessageId
        response = self.call('messages.getHistory', **params)

        for userType in ['profiles', 'groups']:
            if userType not in response: continue

            profiles = response[userType]
            for profile in profiles:
                self.parseUser(profile)

        items = response['items']
        for msg in items:
            result.append(self.parseMsg(msg))

        return result        

    def getMsgsById(self, msgsIds):
        result = []
        ids = ''

        for id in msgsIds:
            ids += str(id)+","

        response = self.call('messages.getById', message_ids=ids, extended=1)

        for item in response['items']:
            result.append(self.parseMsg(item)) 

        if len(response['items']) == 0:
            msg = Msg()
            msg.deleted = True
            result.append(msg)

        return result

    def getMsgById(self, msgId) -> Msg:
        return self.getMsgsById([msgId])[0]

    def getGroup(self, id) -> User:
        for user in self.usersCache:
            if user.id == id:
                return user
        #if id < 0: 
        #    group_id = id*-1
        #else:
        #    group_id = id
        #if id > 0: id = id*-1

        response = self.call('groups.getById',group_id=id*-1)[0]
        user = User()
        user.id = id
        user.firstName = response['name']
        user.lastName = ''
        user.image = self.loadAttach(id, AttachTypes.PHOTO, response['photo_50'])

        return user

    def getUser(self, id) -> User:
        return self.getUsers([id])[0]

    def getUsers(self, ids): 
        userIds = ''
        result = []
        exists = False
        
        for id in ids:
            if id < 0: 
                result.append(self.getGroup(id))
                continue

            exists = False
            for user in self.usersCache:
                if user.id == id:
                    result.append(user)
                    exists = True
                    break
            if not exists:
                userIds += str(id)+','

            if userIds != '':
                params = {}
                params['fields'] = 'photo_50, last_seen'

                if userIds != '-1,': #узнать бы что ето значит... #todo
                    params['user_ids'] = userIds
                
                response = self.call('users.get', **params)
                for userObject in response:
                    result.append(self.parseUser(userObject))
        
        return result

    def parseUser(self, data) -> User:
        result = User()
        result.id = data['id']

        for user in self.usersCache:
            if user.id == data['id']:
                result = user
                return result

        if 'type' in data:
            if ((data['type'] == 'group') or 
                (data['type'] == 'page')  or
                (data['id'] < 0)):

                result = self.parseGroup(data)
                return result

        result.firstName = data['first_name']
        result.lastName = data['last_name']
        result.image = self.loadAttach(data['id'], AttachTypes.PHOTO, data['photo_50'])

        self.usersCache.append(result)
        return result

    def addUser(self, user):
        for i in self.usersCache:
            if i.id == user.id: return
        self.usersCache.append(user)

    def parseGroup(self, data) -> User:
        if ((data['type'] == 'group') or (data['type'] == 'page')):
            result = User()
            result.id = data['id'] * -1
            result.firstName = data['name']
            result.lastName = ''
            result.image = self.loadAttach(result.id, AttachTypes.PHOTO, data['photo_50'])

            self.addUser(result)
            return result
        else:
            raise Exception('Объект не группы не должен тут появляться')

    def parseDeletedMsg(self, data):
        result = Msg()
        result.id = data[1]
        result.peerId = data[3]
        result.fromId = self.getUser(int(data[6]['from']))
        result.attachments = []
        result.reply = []
        result.date = time.time()
        result.text = '<b>Сообщение удалено: </b>'+data[5]

        return result

    def parseMsg(self, data):
        result = Msg()
        
        if 'id' in data:
            result.id = data['id']
            result.text = data['text']
            result.fromId = self.getUser(data['from_id']) 
            result.peerId = data['peer_id']
            result.date = data['date']
            result.attachments = []
            result.reply = []
        else:
            result.id = -1
            result.text = data['text']
            result.fromId = self.getUser(data['from_id']) 
            result.peerId = -1
            result.date = data['date']
            result.attachments = []
            result.reply = []  

        if 'reply_message' in data:
            reply_msg = self.parseMsg(data['reply_message'])
            result.reply.append(reply_msg)
        if 'fwd_messages' in data:
            for reply in data['fwd_messages']:
                reply_msg = self.parseMsg(reply)
                result.reply.append(reply_msg)

        for attachmentsObj in data['attachments']:
            if attachmentsObj['type'] == 'sticker':
                attachment = Attachment()

                sizes = attachmentsObj['sticker']['images_with_background']
                attachment.url = sizes[-1]['url']
                attachment.name = attachmentsObj['sticker']['sticker_id']
                attachment.preview = self.loadAttach(attachment.name, AttachTypes.STICKER, attachment.url)
                attachment.attachType = AttachTypes.STICKER

                result.attachments.append(attachment)

            if attachmentsObj['type'] == 'photo':
                sizes = attachmentsObj['photo']['sizes']
                photoUrl = self.getPhotoUrl(sizes, PhotoSize.MEDIUM)

                attachment = Attachment()
                attachment.url = self.getPhotoUrl(sizes)
                attachment.name = self.getAttachmentName(attachmentsObj)
                attachment.preview = self.loadAttach(attachment.name, AttachTypes.THUMBNAIL, photoUrl)
                attachment.attachType = AttachTypes.PHOTO

                result.attachments.append(attachment)

            if attachmentsObj['type'] == 'doc':
                attachment = Attachment()

                if 'preview' not in attachmentsObj['doc']:
                    attachment.preview = self.loadAttach(
                        'doc.jpg', 
                        AttachTypes.THUMBNAIL, 
                        'https://sun9-57.userapi.com/impg/8eSBy-qs5hGTfda0rMXDzNdsY3TJbKmylFABRg/PB3ANc3ngBg.jpg?size=60x60&quality=96&sign=b2c1b375366032f3dfbc0b947dd90ffe&type=album'
                    )
                else:
                    sizes = attachmentsObj['doc']['preview']['photo']['sizes']
                    attachment.preview = self.loadAttach(
                        self.getAttachmentName(attachmentsObj),
                        AttachTypes.THUMBNAIL,
                        self.getPhotoUrl(sizes, PhotoSize.SMALL)
                    )
                    attachment.url = self.getPhotoUrl(sizes)

                attachment.name = attachmentsObj['doc']['title']
                attachment.url = attachmentsObj['doc']['url']
                attachment.attachType = AttachTypes.DOC
                
                if attachmentsObj['doc']['ext'] == 'gif':
                    attachment.attachType = AttachTypes.GIF

                result.attachments.append(attachment)
                    

        return result

class LongPoll(QtCore.QObject):
    newMsg = QtCore.pyqtSignal(Msg)

    def __init__(self, vkapi: VK_API):
        QtCore.QObject.__init__(self)
        self.vkapi = vkapi

    def updateLP(self):
        LPData = self.vkapi.call('messages.getLongPollServer', lp_version=3)
        self.LPServer = LPData['server']
        self.LPKey = LPData['key']
        self.LPts = int(LPData['ts'])

    def start(self):
        self.updateLP()

        while(True):
            response = requests.get('https://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=3'.format(
                self.LPServer, self.LPKey, self.LPts
            )).json()

            if ('failed' in response):
                failedNum = response['failed']
                if failedNum == 1:
                    self.LPts = int(response['ts'])
                    continue

                if (failedNum == 2) or (failedNum == 3):
                    self.updateLP()
                    continue

            self.LPts = int(response['ts'])
            for event in response['updates']:
                if int(event[0]) != 4: continue

                msg = self.vkapi.getMsgById(event[1])
                if msg.deleted == True:
                    msg = self.vkapi.parseDeletedMsg(event)

                self.newMsg.emit(msg)