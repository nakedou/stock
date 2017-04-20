import MySQLdb


def init_db(dev_mode=True):
    if dev_mode:
        return MySQLdb.connect("localhost", "root", "", "stock_dev", charset="utf8")
    return MySQLdb.connect("localhost", "root", "1215225", "stock", charset="utf8")
