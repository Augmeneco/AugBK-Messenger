from enum import Enum
from PyQt6 import QtCore, QtNetwork, QtGui

import requests, os, time, re
from datetime import datetime

class AttachTypes(Enum):
    PHOTO = 1
    VIDEO = 2
    AUDIO = 3
    DOC = 4
    WALL= 5
    STICKER = 6 
    THUMBNAIL = 7
    GIF = 8
    REPLY = 9
    FORWARD = 10

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
    isReply = False

class Chat:
    id: int
    name: str
    previewMsg: Msg
    image: QtGui.QPixmap
    type: str
    unread: int


class VK_API(QtCore.QObject):
    newDebugMessage = QtCore.pyqtSignal(str)
    networkError = QtCore.pyqtSignal(str)

    def __init__(self, access_token):
        QtCore.QObject.__init__(self)

        self.access_token = access_token
        self.version = 5.131
        self.usersCache = []
        self.chatsCache = {}

        self.requests = ProtectedRequests()
        self.requests.logging.connect(self.logging)

    def logging(self, text):
        print(datetime.today().strftime("%H:%M:%S")+' | '+text)
        self.newDebugMessage.emit(text)

    def call(self, method, **parameters):
        self.logging('Call method '+method)
        url = 'https://api.vk.com/method/' + method
        parameters['access_token'] = self.access_token

        if 'v' not in parameters:
            parameters['v'] = self.version

        result = self.requests.post(url, params=parameters).json()

        if 'error' in result:
            if result['error']['error_code'] == 6 or result['error']['error_code'] == 10:
                time.sleep(2)
                self.logging('Forced sleep')
                return self.call(method, **parameters)


            error_string = 'VK ERROR #{}: "{}"\nPARAMS: {}'.format(result['error']['error_code'],
                                                        result['error']['error_msg'],
                                                        result['error']['request_params'])
            self.logging(error_string)
            raise Exception(error_string)

        return result['response']

    def getAttachmentName(self, data):
        attachType = data['type']

        return attachType + str(data[attachType]['owner_id']) +'_'+ str(data[attachType]['id'])

    def loadAttach(self, name, fileType: AttachTypes, url, noPixMap=False) -> QtGui.QPixmap:
        path = ''
        name = str(name)
        if fileType == AttachTypes.PHOTO:
            path += 'photos/'+name+'.jpg'
        if fileType == AttachTypes.STICKER:
            path += 'stickers/'+name+'.png'
        if fileType == AttachTypes.THUMBNAIL:
            path += 'thumbnails/'+name+'.jpg'
        if fileType == AttachTypes.VIDEO:
            path += '../video/'+name+'.mp4' #ну и что это за костыль
        
        return self.loadPhoto(url, path, noPixMap)

    def loadPhoto(self, url, path, noPixMap=False) -> QtGui.QPixmap:
        self.logging('Loading photo '+path)
        pixMap = QtGui.QPixmap()

        dirPath = '/'.join(('data/images/'+path).split('/')[:-1])
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        if not os.path.exists('data/images/'+path):
            response = self.requests.get(url)
            file = open('data/images/'+path,'wb')
            file.write(response.content)
            file.close()

        if not noPixMap:
            pixMap.load('data/images/'+path)
            return pixMap
        
    def improveMsgText(self, text):
        text = text.replace('<','&lt;').replace('>','&gt;')

        emojiRegex = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\U00010000-\U0010ffff"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                "]+", flags=re.UNICODE)

        if emojiRegex.findall(text):
            outputText = ''
            for char in text:
                if emojiRegex.match(char):
                    try:
                        self.loadPhoto(
                            'https://vk.com/emoji/e/{}.png'.format(char.encode('utf-8').hex()),
                            'emoji/'+char.encode('utf-8').hex()+'.png',
                            noPixMap=True
                        )
                        outputText += '<img src="data/images/emoji/{}.png" alt="{}">'.format(char.encode('utf-8').hex(),char)
                    except: outputText += char
                else:
                    outputText += char
            return outputText
        else: return text

    def getPhotoUrl(self, data, neededSize=PhotoSize.MEDIUM):
        sizes = {}
        for size in data:
            sizes[size['width']+size['height']] = size
        sortedSizes = sorted(sizes)

        if neededSize == PhotoSize.SMALL:
            resultObject = sizes[sortedSizes[0]]
        if neededSize == PhotoSize.MEDIUM:
            resultObject = sizes[sortedSizes[int(len(sortedSizes)/2)]]
        if neededSize == PhotoSize.BIG:
            resultObject = sizes[sortedSizes[-1]]

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
        self.logging('Loading chats {}/{}'.format(offset, response['count']))

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
            if attachmentsObj['type'] == 'video':
                attachment = Attachment()
                #print(attachmentsObj)

                attachment.attachType = AttachTypes.VIDEO

                videosParam = '{}_{}'.format(
                        attachmentsObj['video']['owner_id'],
                        attachmentsObj['video']['id']
                    )
                if 'access_key' in attachmentsObj['video']:
                    videosParam += '_{}'.format(attachmentsObj['video']['access_key'])

                videoInfo = self.call('video.get',
                    videos = videosParam
                )['items'][0]

                if 'external' in videoInfo['files']:
                    attachment.url = videoInfo['files']['external']
                else:
                    videoResolutions = ['mp4_1080', 'mp4_720', 'mp4_480', 'mp4_360', 'mp4_240']
                    for res in videoResolutions:
                        if res in videoInfo['files'].keys():
                            break
                    attachment.url = videoInfo['files'][res]
                    #self.loadPhoto(attachment.url, '../video/'+str(attachmentsObj['video']['id'])+'.mp4')

                attachment.name = '{}_{}'.format(videoInfo['owner_id'], videoInfo['id'])
                attachment.title = videoInfo['title']
                attachment.player = videoInfo['player']
                attachment.preview = self.loadAttach(attachment.name, AttachTypes.THUMBNAIL, self.getPhotoUrl(videoInfo['image']))

                result.attachments.append(attachment)

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

                attachment = Attachment()
                attachment.url = self.getPhotoUrl(sizes, PhotoSize.BIG)
                attachment.name = self.getAttachmentName(attachmentsObj)
                attachment.preview = self.loadAttach(attachment.name, AttachTypes.THUMBNAIL, self.getPhotoUrl(sizes, PhotoSize.MEDIUM))
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
        self.requests = ProtectedRequests()

    def updateLP(self):
        LPData = self.vkapi.call('messages.getLongPollServer', lp_version=3)
        self.LPServer = LPData['server']
        self.LPKey = LPData['key']
        self.LPts = int(LPData['ts'])

    def start(self):
        self.updateLP()

        while(True):
            response = self.requests.get('https://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=3'.format(
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

class ProtectedRequests(QtCore.QObject):
    networkError = QtCore.pyqtSignal(object)
    logging = QtCore.pyqtSignal(str)

    def __init__(self):
        self.requestsSession = requests.Session()
        QtCore.QObject.__init__(self)

    def __getattr__(self, name):
        def method(*args, **kwargs):
            while True:
                try:
                    result = getattr(self.requestsSession, name)(*args, **kwargs)
                    break
                except Exception as E:
                    self.logging.emit(str(E))
                    self.networkError.emit(str(E))

                    time.sleep(2)
                    continue

            return result
        return method