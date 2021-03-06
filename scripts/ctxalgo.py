import sys
from os import path, environ

import requests

sys.path.append(path.dirname(path.dirname(__file__)))

from scripts.database import init_db

URL_PREFIX = 'http://ctxalgo.com'


def get_all_stocks():
    dev_mode = environ.get('ENV') == 'dev'
    db = init_db(dev_mode)
    cursor = db.cursor()
    try:
        r = requests.get(URL_PREFIX + '/api/stocks')
        stocks = r.json()
        for stock_code in stocks:
            j_y_s = stock_code[0:2]
            code = stock_code[2:]
            name = stocks[stock_code]

            cursor.execute("""SELECT * FROM stock WHERE code = '%s'""" % code)
            if cursor.fetchone():
                continue

            cursor.execute("INSERT INTO stock(j_y_s,code,`name`) VALUES (%s, %s, %s)", (j_y_s, code, name))
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    get_all_stocks()



