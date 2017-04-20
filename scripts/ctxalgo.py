import os
import requests

from scripts.database import init_db

URL_PREFIX = 'http://ctxalgo.com'


# get all stock
def get_all_stocks():
    dev_mode = os.getenv('ENV') == 'dev'
    db = init_db(dev_mode)
    cursor = db.cursor()
    try:
        r = requests.get(URL_PREFIX + '/api/stocks')
        stocks = r.json()
        for stock_code in stocks:
            j_y_s = stock_code[0:2]
            code = stock_code[2:]
            name = stocks[stock_code]
            cursor.execute("INSERT INTO stock(j_y_s,code,`name`) VALUES (%s, %s, %s)", (j_y_s, code, name))
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    get_all_stocks()



