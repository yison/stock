import os
import sys
import time
import datetime
import tushare as ts
import pandas as pd
import pymongo
import json
import gflags


def filter_df_col_zero(df, column_name):
    return df[df[column_name] > 0][column_name]

##col_names: list
def filter_df_with_cols(df, col_names):
    return df[col_names]

def get_stocks_with_cols(col_names):
    stocks_df = ts.get_stock_basics()
    sorted_stocks_df = stocks_df.sort_index()
    _df = filter_df_with_cols(sorted_stocks_df, col_names)
    return _df

def get_stocks_with_timeToMarket():
    _df = get_stocks_with_cols(['timeToMarket'])
    time_to_markets = filter_df_col_zero(_df, 'timeToMarket')
    stocks = time_to_markets.apply(format_time)
    return stocks 

def get_stocks():
    _df = get_stocks_with_timeToMarket() 
    return _df.index.values

def format_time(org_time, input_format="%Y%m%d", output_format="%Y-%m-%d"):
    time_array = time.strptime(str(org_time), input_format)
    return time.strftime(output_format, time_array)

## mode: 'w','a'
def download_day_data_by_time(code, path, mode='w', start=None, end=None):
    count = 5
    while(count > 0):
        try:
            #stock_df = ts.get_hist_data(code, start=start, end=end, retry_count=20)
            stock_df = ts.get_k_data(code, start=start,
                                    end=end, retry_count=20)
            stock_df = stock_df.set_index(pd.DatetimeIndex(stock_df['date']))
            #print("@@@@@", stock_df);
            if stock_df is None:
                #print code + ": timeout after retrying 20 times! reget again!"
                count = count - 1
                continue
        except Exception as e:
            print("ERROR:",e)
            count = count - 1
            continue
        else:
            if stock_df is None:
                return None
            else:
                code_path = os.path.join(path, code)
                if 'a' == mode:
                    stock_df.to_csv(code_path, mode=mode, header=False, index=False)
                else:
                    stock_df.to_csv(code_path, mode=mode, index=False) 
                print("code=%s, Done!" % code)
                return code
    return None
             #
            #print datetime.datetime.now()
            #stock_df['date'] = stock_df.index.strftime('%Y%m%d').astype('int')
            # try:
            #     #stock_df.to_csv('/var/lib/influxdb/ssd/stocks/data/history/' + code)
            #     #print stock_df.to_json()
            #     #print datetime.datetime.now()
            #     db.write_points(stock_df, code, tags={'code':code})
            #     #db.write_points(stock_df, code, tags={'code':code}, batch_size=1024)
            #     #print datetime.datetime.now()
            # #    db.stocks[code].insert(json.loads(stock_df.to_json(orient='records')))
            # #    db.stocks[code].create_index([('date', pymongo.DESCENDING)], unique=True)
            # except Exception as e:
            #     print("Error:", e)
            #     return
            #print code + ": Done!"
            # return code
    #print "@@:" + code + ": is not finished"

## day example "2018-02-23"
def download_stock_day_trading_data(path, code, day):
    dir_path = os.path.join(path, day);
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, code); 
    if not os.path.exists(file_path):
        df = ts.get_tick_data(code, date=day, src='tt')
        if df is None or df.dropna().empty:
            return False
        else:
            df.to_csv(file_path)
            return True
    return True

def download_stocks_day_trading_data(path, day):
    stocks = get_stocks()
    count = 5
    for code in stocks:
        while(count > 0):
            try:
                res = download_stock_day_trading_data(path, code, day)
            except Exception as e:
                print ("Download failed:%s:%s" % (code, e)) 
                count = count -1
                time.sleep(1)
                continue 
            else:
                if not res:
                    print ("No trading:%s" % code)
                break

def download_stocks_day_history_data(path):
    stocks_df = get_stocks_with_timeToMarket()
    ##print ("@@:stocks_df", stocks_df);
    ## here code is index 
    for code, start_time in stocks_df.iteritems():
        res = download_day_data_by_time(code, path, start=start_time)
        if res is None:
            print ("Download ERROR: code=%s" % code)

def download_stocks_day_history_inc_data(path, start_time, end_time=None):
    stocks = get_stocks()
    for code in stocks:
        res = download_day_data_by_time(code, path, mode='a', start=start_time, end=end_time)
        if res is None:
            print ("Download ERROR: code=%s" % code)

