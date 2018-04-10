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

FLAGS = gflags.FLAGS

def tracking_model_002(code, df, large_amount_threshold, day, output_file):
    df = df.replace('买盘', 'buy').replace('卖盘', 'sell').replace('中性盘', 'neutral')
    df_trans = df[['time', 'price', 'volume', 'amount', 'type']]
    df_trans = df_trans[df_trans['volume'] > 0].dropna()
    df_trans = df_trans[df_trans['amount'] >= large_amount_threshold]
    df_trans['code'] = code
    df_trans['day'] = day
    df_trans['large_amount_threshold'] = large_amount_threshold
    day_amount = df.amount.sum()
    df_trans['day_amount'] = day_amount 
    df_trans['amount_pct'] = df_trans.amount / day_amount 
    df_trans.to_csv(output_file, header=False, mode='a', index=False)
    return df_trans

