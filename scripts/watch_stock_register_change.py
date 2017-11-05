# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime
from os import path

import requests

sys.path.append(path.dirname(path.dirname(__file__)))
from scripts.wechat import send


def _internal_check(target_stock):
    response = requests.post(target_stock['url'],
                             data={
                                 'org': '63D1B55F525DC58CC6E2E4C0113DB667',
                                 'id': 'B91CA3B55365A0F63223F82048B240C4',
                                 'seqId': '6CBF4D6DE0A570D1F3DB59E191950EDC',
                                 'regNo': '8AF42673C5E1B134AD4066229A44777C3ECA9A89606D782044465A8D6AEB76DD',
                                 'uniScid': 'E7902BA7DBAC9C0286B6F27EADC2E7C9',
                                 'admitMain': 10,
                                 'econKind': 200,
                                 'pageSize': 5,
                                 'curPage': 1
                             })

    if response.status_code != 200:
        return

    res = json.loads(response.text)
    for item in res['data']:
        if item['CHANGE_DATE'] != datetime.utcnow().date().strftime(u'%Y年%m月%d日'):
            continue

        send('企业信息变更提醒', '{0}企业信息已变更。'.format(target_stock['name']))
        break


def stocks_register_change_check():
    target_stocks = [{
        'name': '金利科技',
        'url': 'http://www.jsgsj.gov.cn:58888/ecipplatform/publicInfoQueryServlet.json?queryBgxx=true'
    }]
    for stock in target_stocks:
        _internal_check(stock)
