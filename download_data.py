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

FLAGS = gflags.FLAGS

def format_time(org_time, input_format="%Y%m%d", output_format="%Y-%m-%d"):
    time_array = time.strptime(org_time, input_format)
    return time.strftime(output_format, time_array)

def filter_df_col_zero(df, column_name):
    return df[df[column_name] > 0][column_name]

def get_filter_list():
    return ['000033', '600710', '600732']

def filter_stocks(df, filter_list):
    df.drop(filter_list, inplace=True)

def get_filtered_sorted_stocks():
    stocks_df = ts.get_stock_basics()
    #filter_list = get_filter_list()
    #filter_stocks(stocks_df, filter_list)
    sorted_stocks_df = stocks_df.sort_index()
    sorted_stocks_df.to_csv('data/stocks')
    return sorted_stocks_df

def download_day_data_by_time(code, path, start, end=None):
    start_time = format_time(str(start))
    end_time = format_time(str(end)) if end else None
    count = 5
    while(count > 0):
        try:
            stock_df = ts.get_k_data(code, start=start_time,
                                    end=end_time, retry_count=20)
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
                stock_df.to_csv(code_path)
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

def download_all_stocks_day_data():
    stocks = get_filtered_sorted_stocks()
    stock_list = filter_df_col_zero(stocks, 'timeToMarket')
    count = stocks_counter = len(stock_list)
    for i in range(stocks_counter):
        code = stock_list.index[i]
        hist_day_path = FLAGS.history_day_path
        res = download_day_data_by_time(code, hist_day_path, stock_list[i])
        if res is None:
            count = count - 1
            print ("Download ERROR: code=%s" % code)

def download_all_stocks_week_data():
    pass

def download_all_stocks_month_data():
    pass

def download_all_stocks_quarter_data():
    pass

def download_all_stocks_year_data():
    pass

if __name__=="__main__":
    FLAGS(sys.argv)
    db = engine.get_db_client(FLAGS.mongodb_client)
    start_time = datetime.datetime.now()
    download_all_stocks_day_data()
    end_time = datetime.datetime.now()
    print("begin:", start_time)
    print ("end:", end_time)

