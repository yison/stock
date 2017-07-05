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
app = Celery('tasks', broker='amqp://guest@10.239.131.157//')
app.config_from_object('celeryconfig')

def format_time(org_time, input_format="%Y%m%d", output_format="%Y-%m-%d"):
    time_array = time.strptime(org_time, input_format)
    return time.strftime(output_format, time_array)

@app.task(queue='for_task_A')
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
            if stock_df is None:
                #print code + ": timeout after retrying 20 times! reget again!"
                logger.error('{0}: timeout after retrying 20 times! reget again!'.format(code))
                count = count - 1
                continue
        except Exception, e:
            logger.error(e)
            continue
        else:
            #stock_df.to_csv('data/history/' + code)
            #stock_df['date'] = stock_df.index.strftime('%Y%m%d').astype('int')
            try:
                db.write_points(stock_df, code, tags={'code':code})
                #db.stocks[code].insert(json.loads(stock_df.to_json(orient='records')))
            #    db.stocks[code].create_index([('date', pymongo.DESCENDING)], unique=True)
            except Exception, e:
                logger.error(e) 
            #logger.info('{0} : Done!'.format(code))
            return code 
            #print code + ":Done!"
    #print "@@:" + code + ": is not finished"
    logger.error('{0} is not finished'.format(code))

@app.task(queue='for_task_B')
def create_date_desc_index_in_stock(table):
    db = engine.get_db_client()
    if table:
        try:
            db.stocks[table].create_index([('date', pymongo.DESCENDING)], unique=True)
        except Exception, e:
            logger.error(e)

@app.task(queue='for_realtime')
def download_data_by_realtime(code):
    db = engine.get_db_client()
    try:
        stock_df = ts.get_realtime_quotes(code)
        stock_df = stock_df.drop('name', 1)
        stock_df = stock_df.set_index(pd.DatetimeIndex(stock_df['time']))
        ##TODO:
        #stock_df = stock_df.drop('name', 1)
        #stock_df = stock_df.set_index(pd.DatetimeIndex(stock_df['time']))
        #print("@@@@@", stock_df); 
    except Exception, e:
        logger.error(e)
    try:
        db.write_points(stock_df, code, tags={
                'code': code
                }, database='today')
    except Exception, e:
        logger.error(e)
        return
