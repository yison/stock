#!/usr/bin/env python
import sys
import time
import datetime
from multiprocessing import Pool
import multiprocessing
import tools
import json
import gflags
import easyquotation
from db import engine
#from tasks import download_data_by_realtime
import flags

FLAGS = gflags.FLAGS

def format_time(org_time, input_format="%Y%m%d", output_format="%Y-%m-%d"):
    time_array = time.strptime(org_time, input_format)
    return time.strftime(output_format, time_array)

def filter_df_col_zero(df, column_name):
    return df[df[column_name] > 0][column_name]

def convert(points):
    point_list = []
    for k, v in points.items():
        dict_body = {
            "measurement": k,
            "time": v['time'],
            "tags": {
                "code": k
            },
            "fields": {
                ##TODO:
                "pre_close": v['close'],
                "price": v['price'],
                "high": v['high'],
                "low": v['low'],
                "buy": v['buy'],
                "sell": v['sell'],
                "volume": v['volume'],
                "turnover": v['turnover'],
                "turnover_ratio": v['turnover_ratio'],
                "bid1": v['bid1'],
                "bid1_v": v['bid1_volume'],
                "bid2": v['bid2'],
                "bid2_v": v['bid2_volume'],
                "bid3": v['bid3'],
                "bid3_v": v['bid3_volume'],
                "bid4": v['bid4'],
                "bid4_v": v['bid4_volume'],
                "bid5": v['bid5'],
                "bid5_v": v['bid5_volume'],
                "ask1": v['ask1'],
                "ask1_v": v['ask1_volume'],
                "ask2": v['ask2'],
                "ask2_v": v['ask2_volume'],
                "ask3": v['ask3'],
                "ask3_v": v['ask3_volume'],
                "ask4": v['ask4'],
                "ask4_v": v['ask4_volume'],
                "ask5": v['ask5'],
                "ask5_v": v['ask5_volume'],
                "latest_deal": v['latest_deal'],
                "updown": v['updown'],
                "updown_rario": v['updown_rario'],
                "pe": v['pe'],
                "pb": v['pb'],
                "amplitude": v['amplitude'],
                "circulation_mkt_val": v['circulation_mkt_val'],
                "total_mkt_val": v['total_mkt_val'],
                "high_limit_p": v['high_limit_p'],
                "low_limit_p": v['low_limit_p'],
                "v_ratio": v['v_ratio']
                #"date": v['date']
            }
        }
        point_list.append(dict_body)
    return point_list

def get_realtime_quotation():
    db = engine.get_db_client(FLAGS.influxdb_client)
    ## suport 'sina', 'tencent'/'qq'
    quotation = easyquotation.use(FLAGS.hq_src)
    try:
        points = quotation.market_snapshot()    
        points = convert(points)
    except Exception as e:
        print("ERROR:",e)
    else:
        try:
            db.write_points(points, database='quotation')
        except Exception as e:
            print("Error:", e)
            return

if __name__=="__main__":
    ############
    #Note:
    #need to explicitly to tell flags library to parse argv before you can FLAGS.xxx
    ############
    FLAGS(sys.argv)
    #print (FLAGS.proxy)
    while True:
        get_realtime_quotation()
