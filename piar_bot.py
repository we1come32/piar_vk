"""
Program for piar
Use the user accounts and post on wall any groups.
Text post is random of list "listPosts"
You must write auth data of accounts in mass accountsData
Author Ilya Kanyshev:
  VKontakte: https://vk.com/welc32
  GitHub:    https://github.com/welc32
"""


from time import time, sleep, ctime, strptime
import vk_requests as vk
import threading, json, requests
from random import randint, random


work = True                          # working flag
restart = False                      # restart flag (if True, program work is ended)
flagPiar = False                     # working piar flag 
piarResult = "Пиар не запущен"       # fucking name ))0) (i don't name what is it, but it must be)
groupsPiar = [                       # id group where must posting
    120210647,
    105952064,
    63013736,
    122163002,
    171323685
    ]
usersPiar = []                       # this is must be empty
sleepTime = 2                        # sleep time in error variant get data from integnet
maxCountPotocks = 1                  # maximum count of potoks (maximum - count of processor in your PC)
token = ""                           # access_token for vk
groupId = 0                          # group id
debuging = False                     # flag debuging
adminIds = [147084786, 367833544]    # id admins
v = "5.92"                           # version api
delayReq = 5                         # time after lost connection


# function of getting information about error
# 'e' must be an Exception
def fixError(e):
    s = "Error"
    try:
        tmp = Errors.objects.create(
            date = timezone.now(),
            line = e.__traceback__.tb_lineno,
            directory = str(e.__traceback__.tb_frame.f_code.co_filename),
            description = str(e.args[0]),
        )
        tmp.save()
    except:
        s += " not in DB"
    spisok = [
        ("Description: ", e.args[0],),
        ("Line #",e.__traceback__.tb_lineno,),
        ("Dirrectory: ",e.__traceback__.tb_frame.f_code.co_filename,),
        ("Names: ","\n    "+ ", ".join((str(_)) for _ in e.__traceback__.tb_frame.f_code.co_names)[:])
    ]
    s = "Error"
    for _ in spisok:
        s += "\n  {}{}".format(_[0],_[1])
    print(s)


try:
    class vk_user:
        successList = []
        errorList = []
        def __init__(self, token, id):
            self.token = token
            self.id = id
            self.successList = []
            self.errorList = []
        def vk_login(self):
            try:
                self.api = vk.create_api(service_token=self.token)
                return True
            except Exception as e:
                return False
        def clear(self):
            self.successList = []
            self.errorList = []


    # function error checking from HTTP-codes
    def teststatus(status):
        try:
            if status == 200:
                return True
            elif (status // 100 == 4):
                print("Connecting error_code (#"+str(status)+")")
            elif (status // 100 == 5):
                print("Server error_code (#"+str(status)+")")
            elif (status // 100 == 3):
                print("Redirect error_code (#"+str(status)+")")
            elif (status // 100 == 1):
                print("Information status_code (#"+str(status)+")")
            else:
                print("Status_code not found (#"+str(status)+")")
            return False
        except:
            print("Error finding status_code:", status)
            return False


    # function get local datatime
    def getDate():
        date = strptime(ctime())
        return date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour, date.tm_min, date.tm_sec


    # function get data from Internet
    def get(method_type, method, **params):
        """
            Error codes:

            1 - Error params
            2 - Connect error

            Method_types:

            vk - get vk api method
            sp - other link
        """
        passedList = [
            "messages.getConversationMembers",
            "messages.removeChatUser",
            ]
        if method_type.lower() == "vk":
            url = "https://api.vk.com/method/"
        elif (method_type.lower() == "special") or(method_type.lower() == "sp"):
            url = ""
        else:
            print("Error method_type\n  in function get\n  this params:\n  method_type :", method_type,"\n  method :", method, "\n  **params :", params)
            return -2
        flag = True
        counter = 1
        while flag:
            try:
                file = params.get("file", False)
                if file:
                    del params['file']
                    result = requests.post(url + method, files=file)
                else:
                    result = requests.post(url + method, data=params)
                flag = False
            except Exception as e:
                print("Попытка#"+str(counter),"Адрес "+url + method + " выдает ошибку",e)
                print(" Следующая попытка через", delayReq, "c.")
                sleep(delayReq)
                counter += 1
        if debuging:
            print(url + method, params)
            print(result.status_code, result.text)
        if teststatus(result.status_code):
            if method_type.lower() == "vk":
                data = result.json()
                error = data.get('error', 0)
                if (error == 0):
                    return data.get('response', data)
                else:
                    if method not in passedList:
                        print(error['error_msg'], "this params:")
                        for temp in error['request_params']:
                            try:
                                print("  ", temp['key'], "-", temp['value'])
                            except:
                                print("  ", temp['key'], "-", "Error output data")
                    return -1
            else:
                return result.text
        else:
            print("Connect error")
            return -2


    def piar():
        global flagPiar, piarResult, groupsPiar, work, restart, usersPiar
        try:
            #if True:
            appId = "3116505"
            accountsData = [
                # working |       |              |      |
                # flag    | login |   password   |  id  |
                (True, "88005553535", 'password', 'id',),
            ]
            usersPiar = []
            sCount = 0
            for _ in accountsData:
                if _[0]:
                    try:
                        VKlogin = _[1]
                        VKpassword = _[2]
                        VKid = _[3]
                        tmp = vk_user(
                                vk.create_api(
                                    app_id = appId, 
                                    login = VKlogin, 
                                    password = VKpassword, 
                                    scope = (8192+65536+262144)
                                    )._session._access_token, 
                                VKid
                                )
                        if tmp.vk_login():
                            usersPiar.append(tmp)
                            sCount+=1
                    except Exception as e:
                        fixError(e)
            delay = 180
            randomDelay = 30
            listPosts = [
                ("Доброго времени суток. В нашу беседу ведётся набор активных и веселых ребят, которые умеют поддержать разговор &#128579; \nЕсли ты относишься к числу таких людей, то заглядывай к нам, тебе понравится &#128521; &#128158; \n ⚠Ссылка на беседу в закрепе⚠","")
                ]
            posts = {}
            attachments = {}
            count_posts = 0
            for text, attachment in listPosts:
                if True:
                    posts[count_posts] = text
                    attachments[count_posts] = attachment
                    count_posts += 1
            count_groups = len(groupsPiar)
            i = 0
            print(0)
            while work and (restart == False):
                while flagPiar and work and (restart == False):
                    try:
                        #if True:
                        (day, month, year, hour, minutes, sec) = getDate()
                        error = True
                        for user in usersPiar:
                            user.clear()
                            for group in groupsPiar:
                                messId = randint(0, count_posts-1)
                                mess = posts[messId]
                                attachment = attachments[messId]
                                try:
                                    tmp = user.api.wall.post(owner_id=-group, from_group=0, message=mess, attachments=attachment)
                                    print("https://vk.com/wall-{club}_{tmp}".format(tmp=tmp['post_id'], club=group))
                                    user.successList.append(group)
                                except Exception as e:
                                    print("Error")
                                    user.errorList.append(group)
                            tmpTime = time()
                            while (restart == False) and (tmpTime + (delay+randint(-randomDelay//2,randomDelay//2))//sCount > time()):
                                continue
                    except Exception as e:
                        fixError(e)
        except Exception as e:
            fixError(e)


    while True:
        try:
            q = -2
            work = True
            restart = False
            (day, month, year, hour, minutes, sec) = getDate()
            while (q == -2) and work and (restart == False):
                q = get("vk", "groups.getLongPollServer", access_token=token, v=v, group_id=groupId)
                if (q == -2) or (q == -1):
                    sleep(sleepTime)
                else:
                    ts = q.get('ts')
                    pt = [0]*(maxCountPotocks)
                    t = threading.Thread(target=piar, name="Piar")
                    t.start()
                    lastPotocs = 0
                    while work and (restart == False):
                        (day, month, year, newHour, minutes, sec) = getDate()
                        if debuging == False:
                            restart = (hour != newHour)
                        if work and (restart == False):
                            data = get("sp", q['server'], act='a_check', key=q['key'], ts=ts)
                            if data not in [-1,-2]:
                                data = json.loads(data)
                                ts = data.get('ts', False)
                                updates = data.get('updates', False)
                                if (updates != False) and (updates != None) and (ts != False) and (ts != None):
                                    if work:
                                        for upd in updates:
                                            try:
                                                if (upd['type'] == 'message_new'):
                                                    obj = upd['object']
                                                    peer_id = obj['peer_id']
                                                    user_id = obj['from_id']
                                                    if user_id in adminIds:
                                                        (day, month, year, hout, minutes, sec) = getDate()
                                                        mess = ""
                                                        text = obj['text'].split()
                                                        if len(text)==0:
                                                            continue
                                                        if text[0]=="info":
                                                            mess = "Working status: {flag}\n".format(flag=flagPiar)
                                                            if flagPiar:
                                                                try:
                                                                    for api in usersPiar:
                                                                        if len(api.errorList)>0:
                                                                            _mess = "\n\nДля @id{id}(него) были ошибки отправки в группы:\n".format(id=api.id)
                                                                            tmp = "".join("@club"+str(_)+", " for _ in api.errorList)[:-2]
                                                                            _mess += tmp
                                                                        else:
                                                                            _mess = "\n\nДля @id{id}(него) не было ошибок отправки в группы.".format(id=api.id)
                                                                        mess += _mess
                                                                except Exception as e:
                                                                    fixError(e)
                                                        elif text[0] == "on":
                                                            if flagPiar:
                                                                mess = "Бот уже запущен"
                                                            else:
                                                                flagPiar = True
                                                                mess = "Success"
                                                        elif text[0] == "off":
                                                            if flagPiar == False:
                                                                mess = "Бот уже остановлен"
                                                            else:
                                                                flagPiar = False
                                                                mess = "Success"
                                                        if mess != "":
                                                            get('vk','messages.send',access_token=token,random_id=randint(1, 9999999),v=v,peer_id=peer_id, message=mess)
                                            except Exception as e:
                                                fixError(e)
                                    if restart == False:
                                        continue
                            work = True
                        if restart:
                            work = False
        except Exception as e:
            fixError(e)
            input()
except Exception as e:
    fixError(e)
input()
