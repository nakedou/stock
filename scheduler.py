import schedule


def run_check():
    print('.')

schedule.every(1).minutes.do(run_check)
schedule.every().hour.do(run_check)
schedule.every().day.at("10:30").do(run_check)
schedule.every().day.at("11:30").do(run_check)
schedule.every().day.at("13:30").do(run_check)
schedule.every().day.at("14:30").do(run_check)


while True:
    schedule.run_pending()