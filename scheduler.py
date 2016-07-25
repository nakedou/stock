import schedule

from database import store_real_time_data, print_var_stocks


def run_check():
    print_var_stocks()

schedule.every(5).minutes.do(store_real_time_data)
schedule.every().hour.do(run_check)
schedule.every().day.at("10:30").do(run_check)
schedule.every().day.at("11:30").do(run_check)
schedule.every().day.at("13:30").do(run_check)
schedule.every().day.at("14:30").do(run_check)


while True:
    schedule.run_pending()
