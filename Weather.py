import urllib.request
import gzip
import json

def getWeather(city):
	global weather
	url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(city)
	data = urllib.request.urlopen(url).read()
	data = gzip.decompress(data).decode('utf-8')
	dict = json.loads(data)
	if dict.get('status') == 1002:
		return 'Error：您输入的城市有误'
	elif dict.get('status') == 1000:
		weather = '城市：' + dict.get('data').get('city') + '\n' + '温度：' + dict.get('data').get(
			'wendu') + '\n' + '感冒：' + dict.get('data').get('ganmao') + '\n' + '最高温：' + dict.get('data').get('forecast')[
					  0].get('high') + '\n' + '最低温：' + dict.get('data').get('forecast')[0].get('low') + '\n' + '风向：' + \
				  dict.get('data').get('forecast')[0].get('fengxiang') + '\n' + '风力：' + \
				  dict.get('data').get('forecast')[0].get('fengli') + '\n' + '天气：' + dict.get('data').get('forecast')[
					  0].get('type') + '\n' + '日期：' + dict.get('data').get('forecast')[0].get('date') + '\n' + '-' * 20
	return weather
