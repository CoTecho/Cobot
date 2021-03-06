import random
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio
import CMAWeather
import GetConfigs

from graia.application.message.elements.internal import Plain, At
from graia.application.friend import Friend
from graia.application.group import Group, Member

QQconfFile = "./config/Cobot/QQServe.yml"
WeatherFile = "./config/Cobot/WeatherList.yml"

loop = asyncio.get_event_loop()


def getAt(msg):
    msgString = msg.asDisplay()
    idList = []
    atList = msg.get(At)
    for at in atList:
        msgString = msgString.replace(at.display, '')
        idList.append(at.target)
    return idList, msgString


f = open('data.txt', encoding='utf-8', errors='ignore')
line = f.readline()
sample = '	'
chengyuku = []
while line:
    # print(type(line))
    # print(sample)
    chengyu = []
    index_1 = line.find(sample)
    # print(index_1)
    index_2 = line.find(sample, index_1 + 1)
    # print(line[index_2:])
    ci = line[:index_1]
    pinyin = line[index_1 + 1:index_2].split("'")
    jieshi = line[index_2 + 1:-1]
    chengyu.extend([ci, pinyin, jieshi])
    chengyuku.append(chengyu)
    line = f.readline()
f.close()
game = 0
number = len(chengyuku)
print(number)


def chengyu_compar(now, next):
    if now[1][-1] == next[1][0]:
        return True
    else:
        return False


QQConfig = GetConfigs.getConf(QQconfFile)
QQserver = "http://" + QQConfig["http"] + ":" + str(QQConfig["port"])
BotId = QQConfig["account"]
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=QQserver,  # 填入 httpapi 服务运行的地址
        authKey=QQConfig["authKey"],  # 填入 authKey
        account=BotId,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


# @bcc.receiver("FriendMessage")
# async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
#	await app.sendFriendMessage(friend, MessageChain.create([
#		Plain("Hello, World!")
#	]))

@bcc.receiver("GroupMessage")
async def Indeed(app: GraiaMiraiApplication, group: Group, mesg: MessageChain):
    msg = getAt(mesg)[1]
    if '确实' in msg:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text='确实')]))
        pass


@bcc.receiver("GroupMessage")
async def IndeedNext(app: GraiaMiraiApplication, group: Group, mesg: MessageChain):
    msg = getAt(mesg)[1]
    if '下次一定' in msg:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text='下次一定')]))
        pass


@bcc.receiver("GroupMessage")
async def GoodNight(app: GraiaMiraiApplication, group: Group, mesg: MessageChain):
    msg = getAt(mesg)[1]
    if msg == '晚安':
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text='晚安')]))
        pass


@bcc.receiver("GroupMessage")
async def GetHelp(app: GraiaMiraiApplication, group: Group, mesg: MessageChain):
    msg = getAt(mesg)[1]
    if msg == '帮助':
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text='帮助参见：https://github.com/CoTecho/Cobot/blob/master/README.md')]))
        pass


@bcc.receiver("GroupMessage")
async def Star(app: GraiaMiraiApplication, group: Group, mesg: MessageChain, member: Member):
    weatherList = GetConfigs.getConf(WeatherFile)
    msg = getAt(mesg)[1]
    if (msg == '观星' or msg == '早'):
        weather = CMAWeather.getWeather(weatherList[str(member.id)])
        if not weather:
            weather = weatherList[str(member.id)] + '暂时查不到哦，快使用指令更新你的位置吧！'
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text=weather)]))
    pass


@bcc.receiver("GroupMessage")
async def ChangeWeather(app: GraiaMiraiApplication, group: Group, mesg: MessageChain, member: Member):
    # locCity.txt
    weatherList = GetConfigs.getConf(WeatherFile)
    atid, msg = getAt(mesg)
    msg = msg.replace(' ', '')
    if atid != []:
        if str(atid[0]) == BotId and msg[:2] == "我在":
            newcity = msg[2:]
            weather = CMAWeather.getWeather(newcity)
            if not weather:
                weather = newcity + '暂时查不到哦。'
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain(text=weather)]))
            else:
                weatherList[str(member.id)] = newcity
                GetConfigs.writeConf(WeatherFile, str(member.id), newcity)
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain(text=weather)]))

    pass


@bcc.receiver("GroupMessage")
async def SearchWeather(app: GraiaMiraiApplication, group: Group, mesg: MessageChain):
    atid, msg = getAt(mesg)
    msg = msg.replace(' ', '')
    if atid != []:
        if str(atid[0]) == BotId and msg[:1] == "查":
            city = msg[1:]
            weather = CMAWeather.getWeather(city)
            if not weather:
                weather = city + '暂时查不到哦。'
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain(text=weather)]))
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain(text=weather)]))
    pass


@bcc.receiver("GroupMessage")
async def Games(app: GraiaMiraiApplication, group: Group, mesg: MessageChain):
    # print(mesg.asDisplay())
    global game, chengyu_now, chengyu_next
    if game == 0 and mesg.asDisplay() == "开始":
        game = 1
        chengyu_now = chengyuku[random.randint(0, number - 1)]
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text='从："' + chengyu_now[0] + '"开始')
        ]))
        pass
    if mesg.asDisplay() == '结束' and game != 0:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text='已结束')
        ]))
        game = 0
        pass
    if game == 1 and mesg.asDisplay() == '不会':
        chengyu_list = []
        for _ in chengyuku:
            if chengyu_compar(chengyu_now, _):
                chengyu_list.append(_)
        chengyu_now = chengyu_list[random.randint(0, len(chengyu_list) - 1)]
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text='我接：' + chengyu_now[0])
        ]))
        pass
    if game == 1 and mesg.asDisplay() == '解释':
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text=chengyu_now[0] + '(' + "'".join(chengyu_now[1]) + '):' + chengyu_now[2])
        ]))
        pass
    if game == 1:
        chengyu = mesg.asDisplay()
        for word in chengyuku:
            if chengyu == word[0]:
                chengyu_next = word
                if chengyu_compar(chengyu_now, chengyu_next):
                    if chengyu_next[0] == '一个顶俩':
                        await app.sendGroupMessage(group, MessageChain.create([
                            Plain(text='不要一个顶俩!')
                        ]))
                        game = 0
                        pass
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain(text=chengyu_next[0] + ' 正确!')
                    ]))
                    chengyu_now = chengyu_next
                    pass
                break
    pass


@bcc.receiver("GroupMessage")
async def SearchWord(app: GraiaMiraiApplication, group: Group, mesg: MessageChain):
    atid, msg = getAt(mesg)
    msg = msg.replace(' ', '')
    if atid != []:
        if str(atid[0]) == BotId and msg[:1] == "词":
            word = msg[1:]
            for index in range(number):
                if word == chengyuku[index][0]:
                    await app.sendGroupMessage(group, MessageChain.create([
                        Plain(
                            text=chengyuku[index][0] + '(' + "'".join(chengyuku[index][1]) + '):' + chengyuku[index][2])
                    ]))
                    break
            else:
                await app.sendGroupMessage(group, MessageChain.create([
                    Plain(text='“' + msg[1:] + '”' + "不在词库中哦。")]))
    pass


app.launch_blocking()

# @app.receiver("GroupMessage")
# async def Star(app: Mirai, group: Group, mesg: MessageChain):
#	if mesg.toString()[:2] == '观星':
#		print('已停用')
#		await app.sendGroupMessage(group, [Plain(text='此功能暂时禁用')])
#		pass
#		blognob=0
#		if len(mesg.toString())>2:
#		       blognob=int(mesg.toString()[-1:])
#		NewsFeed = feedparser.parse("http://149.28.225.107:1200/weibo/user/7389593692")
#		print('已观测')
#		entry = NewsFeed.entries[blognob]
#		await app.sendGroupMessage(group, [Plain(text=entry['summary'][:entry['summary'].find('<img src="')].replace('<br>','\n\n'))])
