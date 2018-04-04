#!/usr/bin/env python
"""Defines flags."""

import gflags

##########
## support string/integer/boolean/enum
##########
gflags.DEFINE_string('hq_src', 'tencent',
                     'suport source from sina, tencent/qq')
gflags.DEFINE_string('host', '10.239.131.215',
                     'host server')
gflags.DEFINE_string('port', '8086',
                     'listening port of DB')
gflags.DEFINE_integer('db_connection_retries', 5,
                     'DB connection retrying times')
gflags.DEFINE_string('influxdb_client', 'influxdb',
                     'influxdb client')
gflags.DEFINE_string('influxdb_dataframe_client', 'influxdb_dataframe',
                     'influxdb dataframe client')
gflags.DEFINE_string('mongodb_client', 'mongodb',
                     'mongodb client')
gflags.DEFINE_string('time_type_day', 'D', 
                     'time type:day')
gflags.DEFINE_string('history_export_file_type', 'csv', 
                     'file type:csv')
gflags.DEFINE_string('history_path', 'data/history', 
                     'the path of hisory data')
gflags.DEFINE_integer('record_size', 32,
                      'parsing record size')
gflags.DEFINE_string('sh_stock_prefix', 'sh60',
                     'Shanghai market stock prefix')
gflags.DEFINE_string('sz_stock_prefix', 'sz000',
                     'Shenzhen market stock prefix')
gflags.DEFINE_string('zxb_stock_prefix', 'sz002',
                     'Zhongxiaoban market stock prefix')
gflags.DEFINE_string('cyb_stock_prefix', 'sz300',
                     'Chuangyeban market stock prefix')
gflags.DEFINE_string('raw_day_path', '/home/cloud001/ly/mygithub/stock/data/raw/day',
                     'raw day stock file path')
gflags.DEFINE_string('history_day_path', 
                     '/home/cloud001/ly/mygithub/stock/data/history/day',
                     'day history path')
gflags.DEFINE_string('trading_histroy_day_data_path', 
                     '/home/cloud001/ly/mygithub/stock/data/trading/history/day',
                     'day trading history data path')
gflags.DEFINE_string('trading_histroy_day_tracking_file', 
                     'tracking_trading_day.csv',
                     'the file name of tracking day trading')
