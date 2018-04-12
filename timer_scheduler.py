import os
import sys
import tushare as ts
import pandas as pd
import numpy as np
import utils
import gflags
import flags
import datetime
import csv
import logging
import logging.handlers
from apscheduler.schedulers.background import BlockingScheduler 
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from models import tracking_model_001
from downloads.manager import download_stocks_day_trading_data 
from downloads.manager import download_stocks_day_history_inc_data
from downloads.manager import download_stocks_day_history_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_handler = logging.handlers.RotatingFileHandler('/tmp/stocks.log', 'a', 1000*1000*1000, 3)
logger.addHandler(log_handler)

executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
        'coalesce': False,
        'max_instances': 5
}

scheduler = BlockingScheduler(executors=executors, job_defaults=job_defaults)

FLAGS = gflags.FLAGS

@scheduler.scheduled_job('cron',
                         day_of_week='0-4', 
                         hour='15',
                         minute="35",
                         second="0")
def download_day_trading_detail_job():
    logger.info('download_day_trading_detail_job')
    day = utils.today()
    if utils.is_workday(day):
        path = FLAGS.trading_histroy_day_data_path
        download_stocks_day_trading_data(path, day)
        logging.info('download_day_trading_detail_job:Done')
    else:
        logging.info('Today is not workday')

@scheduler.scheduled_job('cron',
                         day_of_week='0-4', 
                         hour='19',
                         minute="0",
                         second="0")
def download_day_history_job():
    logger.info('download_day_history_job')
    day = utils.today()
    if utils.is_workday(day):
        path = FLAGS.history_day_path
        download_stocks_day_history_data(path)
        logging.info('download_day_history_job:Done')
    else:
        logging.info('Today is not workday')

#TODO: need to consider XD or others
#@scheduler.scheduled_job('cron',
#                         day_of_week='0-4', 
#                         hour='19',
#                         minute="0",
#                         second="0")
#def download_day_history_increment_job():
#    logger.info('download_day_history_increment_job')
#    day = utils.today()
#    if utils.is_workday(day):
#        path = FLAGS.history_day_path
#        download_stocks_day_history_inc_data(path, day)
#        logging.info('download_day_history_increment_job:Done')
#    else:
#        logging.info('Today is not workday')
@scheduler.scheduled_job('cron',
                         day_of_week='0-4', 
                         hour='15',
                         minute="50",
                         second="0")
def run_tracking_model_001_job():
    logger.info("run_tracking_model_001_job")
    max_count = 5
    path = FLAGS.trading_histroy_day_data_path 
    day = utils.today() 
    day_path = os.path.join(path, day)
    file_mapping_list = utils.find_files(day_path)
    file_name = FLAGS.trading_histroy_day_tracking_file
    output_file = os.path.join(path, file_name)
    for (code, file_path) in file_mapping_list:
        df = pd.read_csv(file_path)
        res = tracking_model_001.tracking_model_001_filtered(code, df, max_count, day, output_file)
        if len(res) > 0:
            logger.info(code)
            logger.info(res)
    logger.info("run_tracking_model_001_job:Done!")


if __name__=="__main__":
    FLAGS(sys.argv)
    scheduler.start()
