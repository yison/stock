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
def download_data_by_time(code, start, end=None):
    start_time = format_time(str(start))
    end_time = format_time(str(end)) if end else None
    #db = engine.get_db_client()
    count = 10
    while(count > 0):
        try:
            stock_df = ts.get_h_data(code, start=start_time,
                                    end=end_time, retry_count=20)
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
            #try:
            #    db.stocks[code].insert(json.loads(stock_df.to_json(orient='records')))
            #    db.stocks[code].create_index([('date', pymongo.DESCENDING)], unique=True)
            #except Exception, e:
            #    logger.error(e) 

            #print code + ":Done!"
            return
    #print "@@:" + code + ": is not finished"
    logger.error('{0} is not finished'.format(code))

