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
    filter_list = get_filter_list()
    filter_stocks(stocks_df, filter_list)
    sorted_stocks_df = stocks_df.sort_index()
    sorted_stocks_df.to_csv('data/stocks')
    return sorted_stocks_df

if __name__=="__main__":
    stocks = get_filtered_sorted_stocks()
    stock_list = filter_df_col_zero(stocks, 'timeToMarket')
    print stock_list.shape
    time_to_market_list = zip(stock_list.index, stock_list.values)    

    start_time = datetime.datetime.now()

    for i in range(len(stock_list)):
        result = download_data_by_time.delay(stock_list.index[i],
                                            stock_list[i])

    while not result.ready():
        time.sleep(30)
    end_time = datetime.datetime.now()
    print start_time
    print end_time

