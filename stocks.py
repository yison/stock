#!/opt/anaconda2/bin/python
import time 
import datetime
import tushare as ts
import pandas as pd
from multiprocessing import Pool
import multiprocessing
import tools
import pymongo
from pymongo import MongoClient
import json
from db import engine
from tasks import * 
from celery import chain
    

def format_time(org_time, input_format="%Y%m%d", output_format="%Y-%m-%d"):
    time_array = time.strptime(org_time, input_format)  
    return time.strftime(output_format, time_array)

def get_filter_list():
    return ['000033', '600710', '600732']

def filter_stocks(df, filter_list):
    df.drop(filter_list, inplace=True)

def get_filtered_sorted_stocks():
    stocks_df = ts.get_stock_basics() 
    filter_list = get_filter_list()
    filter_stocks(stocks_df, filter_list)
    sorted_stocks_df = stocks_df.sort_index()
    sorted_stocks_df.to_csv('data/stocks')    
    return sorted_stocks_df
    
def get_sorted_stocks():
    stocks_df = ts.get_stock_basics() 
    sorted_stocks_df = stocks_df.sort_index()
    sorted_stocks_df.to_csv('data/stocks')    
    return sorted_stocks_df

def get_indexes():
    df = ts.get_index()
    df.to_csv('data/indexes') 
    return df

def get_index_codes():
    df = ts.get_index()
    return df['code']

def download_all_history_data():
    stocks = get_filtered_sorted_stocks()    
    start_time = time.time()
    for idx in stocks.index:
        time_to_market = stocks.ix[idx]['timeToMarket']
        if time_to_market:
            stock_df = ts.get_h_data(idx, start=format_time(str(time_to_market)))
            stock_df.to_csv('data/history/' + idx)
            print idx
        else: continue 
    end_time = time.time() 
    delta_time = end_time - start_time
    print delta_time 

def download_hist_data(stock_tuple):
    stock_code = stock_tuple[0]
    time_to_market = stock_tuple[1]
    #print stock_code
    db = engine.get_db_client()
    count = 10
    while(count > 0):
        try:
            stock_df = ts.get_h_data(stock_code, start=format_time(str(time_to_market)),
                                     retry_count=20)
            if stock_df is None:
                #print stock_code + ": timeout after retrying 20 times! reget again!"
                count = count - 1
                continue 
        except Exception, e:
            print e
            continue
        else:
            #stock_df.to_csv('data/history/' + stock_code)
            #stock_df['date'] = stock_df.index.strftime('%Y%m%d').astype('int')
            #try:
            #    db.stocks[stock_code].insert(json.loads(stock_df.to_json(orient='records')))
            #    db.stocks[stock_code].create_index([('date', pymongo.DESCENDING)], unique=True)
            #except Exception, e:
            #    print e

            #print stock_code + ":Done!"
            return
    #print "@@:" + stock_code + ": is not finished"

#def download_data_by_time(stock_tuple):
#    stock_code = stock_tuple[0]
#    start_time = stock_tuple[1]
#    end_time = stock_tuple[2]
#    #db = MongoClient('localhost', 10001)
#    db = engine.get_db_client()
#    print stock_code 
#    count = 10
#    while(count > 0):
#        try:
#            stock_df = ts.get_h_data(stock_code, start=start_time, end=end_time,
#                                     retry_count=20)
#            if stock_df is None:
#                print stock_code + ": timeout after retrying 20 times! reget again!"
#                count = count - 1
#                continue
#        except Exception, e:
#            print e
#            continue
#        else:
#            #stock_df.to_csv('data1/history/' + stock_code, mode='a', header=None)
#            stock_df['date'] = stock_df.index.strftime('%Y%m%d').astype('int')
#            try:
#                db.stocks[stock_code].insert(json.loads(stock_df.to_json(orient='records')))
#            except Exception, e:
#                print e
#            print stock_code + ":Done!"
#            return
#    print "@@:" + stock_code + ": is not finished"

def download_history_data(item):
    ### item is a tuple
    ###
    ###
    code = item[0]
    start_time = item[1]
    end_time = item[2]
    index = item[3]
    db = engine.get_db_client()
    count = 10
    while(count > 0):
        try:
            if index is True:
                df = ts.get_h_data(code, index=True, start=start_time, retry_count=10)
            else:
                df = ts.get_h_data(code, start=start_time, end=end_time, retry_count=10)
            if df is None:
                count = count - 1
                continue
        except Exception, e:
            print e
            count = count -1
            continue
        else:
            df['date'] = df.index.strftime('%Y%m%d').astype('int')
            try:
                if index is True:
                    db.indexes[code].insert(json.loads(df.to_json(orient='records')))
                    db.indexes[code].create_index([('date', pymongo.DESCENDING)], unique=True)
                else:
                    db.stocks[code].insert(json.loads(df.to_json(orient='records')))
                    db.stocks[code].create_index([('date', pymongo.DESCENDING)], unique=True)
            except Exception, e:
                print e
                count = count - 1
                continue
            else:
                print code + ":Done!"
                return
    print "@@:" + code + ": is not finished"

def filter_df_col_zero(df, column_name):
    return df[df[column_name] > 0][column_name] 
     
def multi_download_hist_data():
    #pool = Pool(multiprocessing.cpu_count())
    #pool = Pool(512)
    pool = Pool(768)
    stocks = get_filtered_sorted_stocks()    
    stock_list = filter_df_col_zero(stocks, 'timeToMarket') 
    print stock_list.shape
    time_to_market_list = zip(stock_list.index, stock_list.values)
    pool.map(download_hist_data, time_to_market_list)
    pool.close()
    pool.join()

def download_total_hist_data_task():
    stocks = get_filtered_sorted_stocks()
    stock_list = filter_df_col_zero(stocks, 'timeToMarket')
    print stock_list.shape

    for i in range(10):
        result = chain(download_data_by_time.s(stock_list.index[i],
                                            stock_list[i]) | 
            create_date_desc_index_in_stock.s(stock_list.index[i]))().get() 

    while not result.ready():
        time.sleep(30)

def multi_download_indexes_hist_data():
    pool = Pool(16)
    #codes = get_index_codes()
    codes = ['000001', '399001', '399005', '399006'] 
    start_time_list = ['1990-12-18', '1991-04-02', '2008-06-29', '2010-05-30']
    end_time = None
    index_tag = True
    length = len(codes)
    #start_time_list = tools.init_list(start_time, codes.shape[0]) 
    end_time_list = tools.init_list(end_time, length) 
    index_tag_list = tools.init_list(index_tag, length)
    tuple_list = zip(codes, start_time_list, end_time_list, index_tag_list)
    pool.map(download_history_data, tuple_list)
    pool.close()
    pool.join()
    
    
#def multi_append_data(start_time, end_time):
#    pool = Pool(16)
#    stocks = get_filtered_sorted_stocks()
#    stock_list = filter_df_col_zero(stocks, 'timeToMarket')
#    print stock_list.shape
#    start_time_list = tools.init_list(start_time, stock_list.shape[0])
#    end_time_list = tools.init_list(end_time, stock_list.shape[0])
#    start_end_time_list = zip(stock_list.index, start_time_list, end_time_list)
#    pool.map(download_data_by_time, start_end_time_list)
#    pool.close()
#    pool.join()

def append_data_by_time(start_time, end_time):
    stocks = get_filtered_sorted_stocks()
    stock_list = filter_df_col_zero(stocks, 'timeToMarket')
    print stock_list.shape
    start_time_list = tools.init_list(start_time, stock_list.shape[0])
    end_time_list = tools.init_list(end_time, stock_list.shape[0])
    start_end_time_list = zip(stock_list.index, start_time_list, end_time_list)
    
 
if __name__ == "__main__":
    #get_stocks() 
    #download_all_history_data()
    start_time = datetime.datetime.now()
    #------download history data in parallel
    #multi_download_hist_data()
    #------download history data in parallel

    #------download total history data by celery 
    download_total_hist_data_task()
    #------download total history data by celery 

    #------append data by time in parallel
    #start = '2016-08-26'
    #end = '2016-08-26'
    #multi_append_data(start, end)
    #------append data by time in parallel

    #------download indexes hisroty data in parallel
    #download_history_data(('000001', '1990-12-17', None, True))
    #multi_download_indexes_hist_data()
    #------download indexes hisroty data in parallel

    #-----test delta dates
    #tools.get_delta_dates('20160810','20160815')
    #-----test delta dates
    end_time = datetime.datetime.now()
    print start_time
    print end_time

