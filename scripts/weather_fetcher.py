# -*- coding: utf-8 -*-

#https://www.heweather.com/
#西安市雁塔区代码 CN101110113
import sys
from os import path

import requests

sys.path.append(path.dirname(path.dirname(__file__)))

from scripts.wechat import send

if __name__ == '__main__':
    city = 'CN101110113'
    key = 'a8503b32d81f4da4a944619fc9218324'
    url = 'https://free-api.heweather.com/v5/weather?city={}&key={}'.format(city, key)

    res = requests.get(url)
    fully_weather = res.json()
    daily_forecast = fully_weather['HeWeather5'][0]['now']
    title = "今日-".format(daily_forecast['cond']['txt'])
    send(title, daily_forecast['wind']['sc'])

