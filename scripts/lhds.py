from time import sleep

import MySQLdb
import requests


URL_PREFIX = 'http://lhb.ipail.com/w8'


def init_db():
    return MySQLdb.connect("localhost", "root", "", "stock_dev", charset="utf8")


def get_stocks_holders():
    db = init_db()
    cursor = db.cursor()
    cursor.execute('select code from stock')

    exception_stocks = set()
    try:
        for stock_code, in cursor.fetchall():
            print(stock_code)
            holders = get_holders(stock_code)
            # sleep 3 seconds between crawl
            sleep(3)
            for holder in holders:
                print(holder)
                try:
                    reg_day = holder.get('Day')
                    holders = holder.get('GDRS', 0)
                    change_percent = holder.get('JSQBH', 0)
                    c_m_j_z = holder.get('CMJZ', 0)

                    # TODO: check if record (stock_code+reg_day) exist
                    cursor.execute("""
                        INSERT INTO stock_holders(stock_code,reg_day,holders,change_percent,c_m_j_z)
                        VALUES ('%s', '%s', %d, '%s', '%s')
                    """ % (stock_code, reg_day, holders, change_percent, c_m_j_z))
                except Exception as e:
                    print(e)
                    exception_stocks.add(stock_code)
                    continue
            db.commit()
    finally:
        print(",".join(exception_stocks))
        cursor.close()
        db.close()


def get_holders(code):
    data = {
        'c': 'YiDianCangWei',
        'a': 'GuDongInfo',
        'StockID': code,
        'st': 63
    }

    r = requests.post(URL_PREFIX + '/api/index.php', data=data)
    result = r.json()
    holders = result.get('List')
    return holders


if __name__ == '__main__':
    get_stocks_holders()
