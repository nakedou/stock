import schedule

from scripts.tushare import go_generate_data, store_real_time_data


def run_check():
    go_generate_data()

schedule.every(5).minutes.do(store_real_time_data())
# schedule.every().hour.do(run_check)
schedule.every().day.at("10:00").do(run_check)
schedule.every().day.at("10:30").do(run_check)
schedule.every().day.at("11:00").do(run_check)
schedule.every().day.at("11:30").do(run_check)
schedule.every().day.at("13:30").do(run_check)
schedule.every().day.at("14:00").do(run_check)
schedule.every().day.at("14:30").do(run_check)


while True:
    schedule.run_pending()
