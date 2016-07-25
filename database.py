#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine
import tushare as ts
import MySQLdb, time

engine = create_engine('mysql://root:@127.0.0.1/stock?charset=utf8')


def store_stock_basics():
    df = ts.get_stock_basics()
    df.to_sql('stock_basics', engine, if_exists='append')


def store_new_stocks_schedule():
    df = ts.new_stocks()
    df.to_sql('ipo_schedule', engine, if_exists='replace')


def store_real_time_data():
    df = ts.get_today_all()
    df.to_sql('real_time_data', engine, if_exists='append')


def init_db():
    db = MySQLdb.connect("localhost", "root", "", "stock", charset="utf8")
    return db


# clear real time data, every day run once
def clear_real_time_data():
    print('clear old real time data...')
    db = init_db()
    cursor = db.cursor()
    cursor.execute("delete from real_time_data")
    db.commit()
    print('clear old real time data end')


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


def print_var_stocks():
    print("current time is: {}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    db = init_db()
    cursor = db.cursor()
    var_samp_sql = "select code, name, VAR_SAMP(changepercent) changed from real_time_data group by code"
    sql = "select code, name from (" + var_samp_sql + ") t " + \
          " where changed > 0 and code not in (" + ",".join(get_exclude_codes()) + ") " + \
          " order by changed limit 20"
    count = cursor.execute(sql)
    if count > 0:
        results = cursor.fetchall()
        for result in results:
            code, name = result
            print("{}   {}".format(code, name.encode('utf-8')))


if __name__ == '__main__':
    # print_var_stocks()
    clear_real_time_data()

