#!/usr/bin/python
# -*- coding: UTF-8 -*-

stocks_map = [
    {'code': '000001', 'name': '平安银行'},
    {'code': '601318', 'name': '中国平安'},
    {'code': '600036', 'name': '招商银行'},
    {'code': '600028', 'name': '中国石化'},
    {'code': '601006', 'name': '大秦铁路'},
    {'code': '601857', 'name': '中国石油'},
    {'code': '601117', 'name': '中国化学'},
    {'code': '601628', 'name': '中国人寿'}
]


def get_exclude_codes():
    codes = [stock['code'] for stock in stocks_map]
    return codes
