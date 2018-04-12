import os
import sys
import time
import datetime
import tushare as ts
import pandas as pd
import gflags
import flags
from downloads.manager import *

FLAGS = gflags.FLAGS


if __name__=="__main__":
    FLAGS(sys.argv)
    start_time = datetime.datetime.now()

    hist_day_path = FLAGS.history_day_path
    #total:
    #download_stocks_day_history_data(hist_day_path)

    #increment
    #start_day = '2018-04-12' 
    #download_stocks_day_history_inc_data(hist_day_path, start_day)

    end_time = datetime.datetime.now()
    print("begin:", start_time)
    print ("end:", end_time)

