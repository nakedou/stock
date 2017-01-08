import MySQLdb


DB_URL = 'mysql://root:@127.0.0.1/stock_dev?charset=utf8'


def init_db():
    return MySQLdb.connect("localhost", "root", "", "stock_dev", charset="utf8")

