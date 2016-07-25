import tushare as ts


def list_stocks():
    return ts.get_today_all()


def get_stock(code):
    df = ts.get_tick_data(code, date='2016-06-10')
    df.head(10)
    return df

if __name__ == '__main__':
    stocks = list_stocks()
    print('this time get stocks count {}'.format(len(stocks)))

    for index in range(len(stocks)):
        line = stocks.iloc[index]
        print('{}       {}         {}'.format(line['code'], line['name'], line['changepercent']))
