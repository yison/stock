#!/opt/anaconda2/bin/python
from celery import Celery
from celery.utils.log import get_task_logger
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


logger = get_task_logger(__name__)
app = Celery('tasks', broker='amqp://guest@10.239.131.155//')
app.config_from_object('celeryconfig')

def format_time(org_time, input_format="%Y%m%d", output_format="%Y-%m-%d"):
    time_array = time.strptime(org_time, input_format)
    return time.strftime(output_format, time_array)

@app.task
def add(x, y):
    return x + y

@app.task
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
            logger.error(e)
            continue
        else:
            #stock_df.to_csv('data/history/' + stock_code)
            stock_df['date'] = stock_df.index.strftime('%Y%m%d').astype('int')
            try:
                db.stocks[stock_code].insert(json.loads(stock_df.to_json(orient='records')))
                db.stocks[stock_code].create_index([('date', pymongo.DESCENDING)], unique=True)
            except Exception, e:
                logger.error(e) 

            #print stock_code + ":Done!"
            return
    #print "@@:" + stock_code + ": is not finished"
    logger.eror('{0} is not finished'.format(stock_code))

