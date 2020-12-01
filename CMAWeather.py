from gzip import decompress
from json import loads
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from socket import timeout
from pandas import read_html
from csv import reader

from bs4 import BeautifulSoup


def transKey2Str(jsonDict):
    # 将键值转为str
    for key in jsonDict:
        if isinstance(jsonDict[key], dict):
            transKey2Str(jsonDict[key])
        else:
            jsonDict[key] = str(jsonDict[key])
            # print(type(jsonDict[key]))
    return jsonDict


def transImg2Weather(data):
    # 将天气图像转为文字
    weatherList = []
    weather = data.find("img").attrs["src"][20:-4]
    return weather


def getCMATable(rawTable):
    # 此函数将CMA网站上的每日天气表读取为数组
    # 格式为 [时间,天气,气温,降水,风速,风向,气压,湿度,云量]
    table = [[], [], [], [], [], [], [], []]
    # print(table)
    rows = rawTable.findAll("tr")
    for row in range(9):
        datas = rows[row].findAll("td")
        for i in range(8):
            table[i].append(datas[i + 1].text)
            if row == 1: table[i][1] = transImg2Weather(datas[i + 1])
            # print(datas[i+1].text)
        # print('换行')
    return table


def getCMARealWeather(cityNum):
    url = 'https://weather.cma.cn/api/now/{}'.format(cityNum)
    try:
        data = urlopen(url).read()
        # data = decompress(data).decode('utf-8')
        dict = loads(data)
        return dict
    except HTTPError:
        # print("不存在编号" + str(cityNum))
        return ''
    except URLError:
        # print("超时重试")
        CMAWeatherTable(cityNum)
    except timeout:
        # print("超时重试")
        CMAWeatherTable(cityNum)


def CMAWeatherTable(cityNum):
    CMAAddr = 'https://weather.cma.cn/web/weather/{}.html'
    try:
        html = urlopen(CMAAddr.format(cityNum), timeout=3)
        weather = {}
        weatherTable = []
        bsObj = BeautifulSoup(html)
        weather["city"] = bsObj.find("div", {"id": "cityPosition"}).findAll("button")[-1].text
        rawTables = bsObj.findAll("table", {"class": "hour-table"})
        # weatherTable=read_html(CMAAddr.format(cityNum))
        for rawTable in rawTables:
            weatherTable.append(getCMATable(rawTable))
        return weatherTable
    except HTTPError:
        # print("不存在编号" + str(cityNum))
        return ''
    except URLError:
        # print("超时重试")
        CMAWeatherTable(cityNum)
    except timeout:
        # print("超时重试")
        CMAWeatherTable(cityNum)


def getCityNum(name):
    #将城市名转换为编号
    citys_file_read = open('citys.txt', mode='r', encoding='utf-8')
    citys = [city for city in reader(citys_file_read)]
    for city in citys:
        if name==city[3]:
            return int(city[0])
    else:
        return 0


def getWeather(city):
    #获取天气
    global weather
    cityNum=getCityNum(city)
    if not cityNum:
        return 0
    jsondict = getCMARealWeather(cityNum)
    # print(type(str(jsondict.get("name"))))
    weatherDict = transKey2Str(jsondict)["data"]["now"]
    if jsondict:
        weather = '城市：' + jsondict['data']["location"]["name"] + '\n'
        # print(weatherDict)
        weather += '温度：' + weatherDict.get("temperature") + '℃\n'
        weather += '湿度：' + weatherDict.get("humidity") + '%\n'
        weather += '气压：' + weatherDict.get("pressure") + 'hPa\n'
        weather += '降水量：' + weatherDict.get("precipitation") + 'mm\n'
        weather += '风向：' + weatherDict.get("windDirection") + '\n'
        weather += '风力：' + weatherDict.get("windScale") + '\n'
        weather += '风速：' + weatherDict.get("windSpeed") + '\n'
        weather += '更新时间：'+jsondict.get("data").get("lastUpdate")
    return weather

