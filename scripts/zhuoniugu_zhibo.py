import json
import sys
from os import path

import requests

sys.path.append(path.dirname(path.dirname(__file__)))

from scripts import wechat

DOMAIN_NAME = 'http://www.zhuoniugu.com'


def get_live_data():
    request_url = '/api.php?c=zhibo&a=new&show=json'
    response = requests.get(DOMAIN_NAME + request_url)
    if response.status_code == 200:
        print(json.loads(response.text)['data']['lists'])
        # wechat.send('success', json.loads(response.text))
    else:
        wechat.send('something goes wrong', response.text)


if __name__ == '__main__':
    get_live_data()
