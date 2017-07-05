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
from tasks import download_data_by_time 


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

def download_data_by_time(code, start, end=None):
    start_time = format_time(str(start))
    end_time = format_time(str(end)) if end else None
    db = engine.get_db_client()
    count = 1
    while(count > 0):
        try:
            stock_df = ts.get_k_data(code, start=start_time,
                                    end=end_time, retry_count=20)
            stock_df = stock_df.set_index(pd.DatetimeIndex(stock_df['date']))
            #print("@@@@@", stock_df); 
            if stock_df is None:
                print code + ": timeout after retrying 20 times! reget again!"
                count = count - 1
                continue
        except Exception, e:
            print("ERROR:",e)
            continue
        else:
            #print datetime.datetime.now()
            #print datetime.datetime.now()
            #stock_df['date'] = stock_df.index.strftime('%Y%m%d').astype('int')
            try:
                stock_df.to_csv('/var/lib/influxdb/ssd/stocks/data/history/' + code)
                #print stock_df.to_json()
                #,date,open,close,high,low,volume,code
                ################################
                 
                json_body = []
                for row in stock_df.itertuples():
                    print row
                    dict_body = { 
                        "measurement": row.code,
                        "time": row.date,
                        #"time": datetime.datetime.now(),
                        "fields": {
                            "date": row.date,
                            "open": row.open,
                            "close": row.close,
                            "high": row.high,
                            "low": row.low,
                            "volume": int(row.volume)
                        }
                    }
                    json_body.append(dict_body);
                print json_body
                #print datetime.datetime.now()
                ##db.write_points(json_body, time_precision='m', tags={"code": code})
                #db.write_points(json_body, tags={"code": code})
                #print datetime.datetime.now()
                ########################################
                ###################
                # dataframe
                print datetime.datetime.now()
                db.write_points(stock_df, code, tags={'code':code}) 
                ##db.write_points(stock_df, code, tags={'code':code}, batch_size=1024)
                ####################
                print datetime.datetime.now()
            #    db.stocks[code].insert(json.loads(stock_df.to_json(orient='records')))
            #    db.stocks[code].create_index([('date', pymongo.DESCENDING)], unique=True)
            except Exception, e:
                print("Error:", e)
                return
            print code + ": Done!"
            return code
    print "@@:" + code + ": is not finished"

if __name__=="__main__":
    start_time = datetime.datetime.now()

    stocks = get_filtered_sorted_stocks()
    stock_list = filter_df_col_zero(stocks, 'timeToMarket')
    #print stock_list 
    #print stock_list.shape
    #pool = Pool(10)
    #pool.map(download_data_by_time, )
    #pool.close()
    #pool.join()
    for i in range(len(stock_list)):
        download_data_by_time(stock_list.index[i],
                                            stock_list[i])

    ## celery
    #for i in range(len(stock_list)):
    #    result = download_data_by_time.delay(stock_list.index[i],
    #                                        stock_list[i])
    end_time = datetime.datetime.now()
    print "begin:", start_time
    print "end:", end_time

