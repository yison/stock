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

def tracking_model_001(code, df, max_count, day, output_file):
## clean data
    df = df.replace('买盘', 'buy').replace('卖盘', 'sell')
    df_trans = df[['time', 'price', 'volume', 'amount', 'type']]
    df_trans = df_trans[df_trans['volume'] > 0].dropna()
    df_trans = df_trans[df_trans['amount'] > 9000]
    head_max_count = df_trans.volume.value_counts().head(max_count)
    count_list = []
    item_list = [] 
    ##['date', 'code', 'type', 'type_pct', 'vol', 'amount_mean', 'total_vol_type_amount', 'amount_pct', 
    ##   'detail_data']
    ##
    for i in head_max_count.index:
        _df = df_trans[df_trans.volume == i]
        _df.time = pd.to_datetime(day + " " + _df.time)
        _df_trans = _df.set_index('time')
        df_count = _df_trans.to_period('T').index.value_counts().rename('mins_count').to_frame()
        #         print (df_count.head())
        df_count_new = df_count[df_count.mins_count > 3].sort_index()
        if (df_count_new.mins_count.count() > 20):
            pct_type = _df_trans.type.value_counts(normalize=True)
            if (pct_type[0] > 0.78):
                count_list.append((i, pct_type.index[0], pct_type[0], df_count_new))
                total_vol_type_amount = pct_type[0] * _df_trans.amount.sum() 
                amount_pct = total_vol_type_amount / df_trans.amount.sum()  
                item = []
                item.append(day)
                item.append(code)
                item.append(pct_type.index[0])
                item.append(pct_type[0])
                item.append(i)
                item.append(_df_trans.amount.mean())
                item.append(total_vol_type_amount)
                item.append(amount_pct)
                item.append(df_count_new)
                item_list.append(item)
    if item_list:
        with open(output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            for item in item_list:
                writer.writerow(item) 
    return (count_list)


def tracking_model_001_filtered(code, df, max_count, day, output_file):
##  clean data
    df = df.replace('买盘', 'buy').replace('卖盘', 'sell')
    df_trans = df[['time', 'price', 'volume', 'amount', 'type']]
    df_trans = df_trans[df_trans['volume'] > 0].dropna()
    df_trans = df_trans[df_trans['amount'] > 9000]
    head_max_count = df_trans.volume.value_counts().head(max_count)
    count_list = []
    item_list = [] 
    ##['date', 'code', 'type', 'type_pct', 'vol', 'amount_mean', 'total_vol_type_amount', 'amount_pct', 
    ## 'day_amount', '10m_detail_data', '20m_detail_data']
    ##
    if len(head_max_count.index) > 2:
        vol1 = head_max_count.index[0]
        vol2 = head_max_count.index[1]
        vol3 = vol1 + vol2
        if vol3 in head_max_count.index:
            _df = df_trans[df_trans.volume.isin([vol1,vol2,vol3])]
            _df.time = pd.to_datetime(day + " " + _df.time)
            _df_trans = _df.set_index('time')
            df_count = _df_trans.to_period('T').index.value_counts().rename('mins_count').to_frame()

            df_resample_10m = df_count.resample('10T').sum().dropna()
            df_resample_10m_filtered = df_resample_10m[df_resample_10m >= 28].dropna()
            df_resample_20m = df_count.resample('20T').sum().dropna()
            df_resample_20m_filtered = df_resample_20m[df_resample_20m >= 56].dropna()
            df_count_new = df_count[df_count.mins_count > 3].sort_index()
            if (df_count_new.mins_count.count() >= 20 and df_resample_10m_filtered.mins_count.count() >= 3 and df_resample_20m_filtered.mins_count.count() >= 1):
                pct_type = _df_trans.type.value_counts(normalize=True)
                if (pct_type[0] > 0.85):
                    count_list.append(([vol1, vol2, vol3], pct_type.index[0], pct_type[0], df_resample_10m_filtered,df_resample_20m_filtered, df_count_new))
                    total_vol_type_amount = pct_type[0] * _df_trans.amount.sum() 
                    day_amount = df_trans.amount.sum()
                    amount_pct = total_vol_type_amount / day_amount 
                    item = []
                    item.append(day)
                    item.append(code)
                    item.append(pct_type.index[0])
                    item.append(pct_type[0])
                    item.append([vol1, vol2, vol3])
                    item.append(_df_trans.amount.mean())
                    item.append(total_vol_type_amount)
                    item.append(amount_pct)
                    item.append(day_amount)
                    item_list.append(item)

    for i in head_max_count.index:
        _df = df_trans[df_trans.volume == i]
        _df.time = pd.to_datetime(day + " " + _df.time)
        _df_trans = _df.set_index('time')
        df_count = _df_trans.to_period('T').index.value_counts().rename('mins_count').to_frame()
        #         print (df_count.head())
        df_resample_10m = df_count.resample('10T').sum().dropna()
        df_resample_10m_filtered = df_resample_10m[df_resample_10m >= 28].dropna()
        df_resample_20m = df_count.resample('20T').sum().dropna()
        df_resample_20m_filtered = df_resample_20m[df_resample_20m >= 56].dropna()
        df_count_new = df_count[df_count.mins_count > 3].sort_index()
        if (df_count_new.mins_count.count() >= 20 and df_resample_10m_filtered.mins_count.count() >= 3 and df_resample_20m_filtered.mins_count.count() >= 1):
            pct_type = _df_trans.type.value_counts(normalize=True)
            if (pct_type[0] > 0.75):
                count_list.append((i, pct_type.index[0], pct_type[0], df_resample_10m_filtered, df_resample_20m_filtered, df_count_new))
                total_vol_type_amount = pct_type[0] * _df_trans.amount.sum() 
                day_amount = df_trans.amount.sum()
                amount_pct = total_vol_type_amount / day_amount 
                item = []
                item.append(day)
                item.append(code)
                item.append(pct_type.index[0])
                item.append(pct_type[0])
                item.append(i)
                item.append(_df_trans.amount.mean())
                item.append(total_vol_type_amount)
                item.append(amount_pct)
                item.append(day_amount)
                item_list.append(item)
    if item_list:
        with open(output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            for item in item_list:
                writer.writerow(item) 
    return (count_list)

def filter_df_col_zero(df, column_name):
    return df[df[column_name] > 0][column_name]

def get_filtered_sorted_stocks():
    stocks_df = ts.get_stock_basics()
    sorted_stocks_df = stocks_df.sort_index()
    return sorted_stocks_df
