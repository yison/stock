#!/opt/anaconda2/bin/python
import time 
import datetime
import tushare as ts
import pandas as pd
from multiprocessing import Pool
import multiprocessing
import tools

def format_time(org_time, input_format="%Y%m%d", output_format="%Y-%m-%d"):
    time_array = time.strptime(org_time, input_format)  
    return time.strftime(output_format, time_array)

def get_sorted_stocks():
    stocks_df = ts.get_stock_basics() 
    sorted_stocks_df = stocks_df.sort_index()
    sorted_stocks_df.to_csv('data/stocks')    
    return sorted_stocks_df

def download_all_history_data():
    stocks = get_sorted_stocks()    
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
    print stock_code
    count = 10
    while(count > 0):
        try:
            stock_df = ts.get_h_data(stock_code, start=format_time(str(time_to_market)),
                                     retry_count=20)
            if stock_df is None:
                print stock_code + ": timeout after retrying 20 times! reget again!"
                count = count - 1
                continue 
        except Exception, e:
            print e
            continue
        else:
            stock_df.to_csv('data/history/' + stock_code)
            print stock_code + ":Done!"
            return
    print "@@:" + stock_code + ": is not finished"

def download_data_by_time(stock_tuple):
    stock_code = stock_tuple[0]
    start_time = stock_tuple[1]
    end_time = stock_tuple[2]
    print stock_code 
    count = 10
    while(count > 0):
        try:
            stock_df = ts.get_h_data(stock_code, start=start_time, end=end_time,
                                     retry_count=20)
            if stock_df is None:
                print stock_code + ": timeout after retrying 20 times! reget again!"
                count = count - 1
                continue
        except Exception, e:
            print e
            continue
        else:
            stock_df.to_csv('data1/history/' + stock_code, mode='a', header=None)
            print stock_code + ":Done!"
            raise
            return
    print "@@:" + stock_code + ": is not finished"
 
    pass

def filter_df_col_zero(df, column_name):
    return df[df[column_name] > 0][column_name] 
     
def multi_download_hist_data():
    #pool = Pool(multiprocessing.cpu_count())
    pool = Pool(16)
    stocks = get_sorted_stocks()    
    stock_list = filter_df_col_zero(stocks, 'timeToMarket') 
    print stock_list.shape
    time_to_market_list = zip(stock_list.index, stock_list.values)
    pool.map(download_hist_data, time_to_market_list)
    pool.close()
    pool.join()

def multi_append_data(start_time, end_time):
    pool = Pool(16)
    stocks = get_sorted_stocks()
    stock_list = filter_df_col_zero(stocks, 'timeToMarket')
    print stock_list.shape
    start_time_list = tools.init_list(start_time, stock_list.shape[0])
    end_time_list = tools.init_list(end_time, stock_list.shape[0])
    start_end_time_list = zip(stock_list.index, start_time_list, end_time_list)
    pool.map(download_data_by_time, start_end_time_list)
    pool.close()
    pool.join()
 
if __name__ == "__main__":
    #get_stocks() 
    #download_all_history_data()
    
    start_time = datetime.datetime.now()
    #------download history data in parallel
    #multi_download_hist_data()
    #------download history data in parallel

    #------append data by time in parallel
    #start = '2016-08-12'
    #end = '2016-08-17'
    #multi_append_data(start, end)
    #------append data by time in parallel

    end_time = datetime.datetime.now()
    print start_time
    print end_time

