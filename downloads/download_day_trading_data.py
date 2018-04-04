import os
import sys
import time
import datetime
import tushare as ts
import pandas as pd
# from multiprocessing import Pool
# import multiprocessing
# import tools
import pymongo
# from pymongo import MongoClient
import json
from db import engine
# from tasks import download_data_by_time
import gflags
import flags
import utils

FLAGS = gflags.FLAGS

def filter_df_col_zero(df, column_name):
    return df[df[column_name] > 0][column_name]

def get_stocks():
    stocks_df = ts.get_stock_basics()
    sorted_stocks_df = stocks_df.sort_index()
    stock_list = filter_df_col_zero(sorted_stocks_df, 'timeToMarket')
    return stock_list.index.values

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

def download_all_stocks_day_trading_data(path, day):
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

if __name__=="__main__":
    FLAGS(sys.argv)
    run_time_start = datetime.datetime.now()
    day = datetime.date.today().strftime("%Y-%m-%d")
    #day="2018-03-02"
    day_list = [
                #'2018-02-22',
                #'2018-02-23',
                #'2018-02-26',
                #'2018-02-27',
                #'2018-02-28',
                #'2018-03-01',
                #'2018-03-02',
                #'2018-03-05',
                #'2018-03-06',
                #'2018-03-07',
                #'2018-03-08',
                #'2018-03-09',
                #'2018-03-12',
                #'2018-03-13',
                #'2018-03-14',
                #'2018-03-15'
                #'2018-03-16'
                #day
               ]
    path = FLAGS.trading_histroy_day_data_path
    #download_all_stocks_day_trading_data(path, day)
    for day in day_list:
        download_all_stocks_day_trading_data(path, day)
    run_time_end = datetime.datetime.now()
    print("begin:", run_time_start)
    print ("end:", run_time_end)

