#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine
import tushare as ts
import MySQLdb
import time

engine = create_engine('mysql://root:@127.0.0.1/stock?charset=utf8')


def store_stock_basics():
    df = ts.get_stock_basics()
    df.to_sql('stock_basics', engine, if_exists='append')


def store_real_time_data():
    print('begin to update real time data......')
    clear_real_time_data()

    df = ts.get_today_all()
    df.to_sql('real_time_data', engine, if_exists='append')
    print('update real time data end')


def init_db():
    db = MySQLdb.connect("localhost", "root", "", "stock", charset="utf8")
    return db


def clear_real_time_data():
    db = init_db()
    cursor = db.cursor()
    cursor.execute("delete from real_time_data")
    db.commit()


# 流通市值小于100亿
def get_exclude_codes():
    db = init_db()
    cursor = db.cursor()
    sql_open_price = "select distinct(code), open from real_time_data"
    sql = "select t1.code, t1.name from stock_basics t1 left join (" + sql_open_price + ") t2" \
          " on t1.code = t2.code where t1.outstanding * t2.open > 1000000"
    cursor.execute(sql)
    results = cursor.fetchall()
    codes = [code for code, name in results]
    return codes


def get_min_price_change_percent_fluctuation_stocks():
    print("current time is: {}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    db = init_db()
    cursor = db.cursor()
    sql = "select code, name from real_time_data" + \
          " where (high-low)/open > 0 and code not in (" + ",".join(get_exclude_codes()) + ") " + \
          " order by (high-low)/open limit 20"
    count = cursor.execute(sql)
    if count > 0:
        results = cursor.fetchall()
        for result in results:
            code, name = result
            print("{}   {}".format(code, name.encode('utf-8')))


if __name__ == '__main__':
    # store_real_time_data()
    get_min_price_change_percent_fluctuation_stocks()
