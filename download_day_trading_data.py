import os
import sys
import time
import datetime
import tushare as ts
import pandas as pd
import pymongo
import json
import gflags
import flags
from downloads.download_day_trading_data import *

FLAGS = gflags.FLAGS

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
                '2015-04-20',
                '2015-04-28',
                '2015-05-28',
                '2015-06-05',
                '2015-06-08',
                '2015-07-06'
                #day
               ]
    path = FLAGS.trading_histroy_day_data_path
    for day in day_list:
        download_all_stocks_day_trading_data(path, day)
    run_time_end = datetime.datetime.now()
    print("begin:", run_time_start)
    print ("end:", run_time_end)

