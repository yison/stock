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

