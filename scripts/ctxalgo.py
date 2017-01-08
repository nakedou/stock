import MySQLdb
import requests


URL_PREFIX = 'http://ctxalgo.com'


def init_db():
    return MySQLdb.connect("localhost", "root", "", "stock_dev", charset="utf8")


# get all stock
def get_all_stocks():
    db = init_db()
    cursor = db.cursor()
    try:
        r = requests.get(URL_PREFIX + '/api/stocks')
        stocks = r.json()
        for key in stocks:
            stock_code = key.encode('utf-8')
            j_y_s = stock_code[0:2]
            code = stock_code[2:]
            name = stocks.get(stock_code).encode('utf-8')

            cursor.execute("INSERT INTO stock(j_y_s,code,`name`) VALUES (%s, %s, %s)", (j_y_s, code, name))
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    get_all_stocks()



