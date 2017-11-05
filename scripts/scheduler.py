import sys
from os import path

import schedule

sys.path.append(path.dirname(path.dirname(__file__)))
from scripts.watch_stock_register_change import stocks_register_change_check


def run_check():
    print('')


def run_stock_register_change_check():
    stocks_register_change_check()

# schedule.every(5).minutes.do(run_check)
# schedule.every().hour.do(run_check)
# schedule.every().day.at("10:00").do(run_check)

schedule.every().day.at("20:30").do(run_stock_register_change_check)


while True:
    schedule.run_pending()
