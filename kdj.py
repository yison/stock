# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd

stock_code_list = []
for root, dirs, files in os.walk('data/all_trading_data/stock_data'):
    if files:
        for f in files:
            if '.csv' in f:
                stock_code_list.append(f.split('.csv')[0])


print "Total stock number is %d" % len(stock_code_list) 
all_jc_sc_price_change_ratio = pd.DataFrame()

for code in stock_code_list:
    #print code

    stock_data = pd.read_csv('data/all_trading_data/stock_data/' + code + '.csv', parse_dates=[1])
    stock_data.sort('date', inplace=True)
    #KDJ
    #calculate the lowest value in 9 days
    low_list = pd.rolling_min(stock_data['low'], 9)
    low_list.fillna(value=pd.expanding_min(stock_data['low']), inplace=True)
    #calculate the highest value in 9 days
    high_list = pd.rolling_max(stock_data['high'], 9)
    high_list.fillna(value=pd.expanding_max(stock_data['high']), inplace=True)
    rsv = (stock_data['close'] - low_list) / (high_list - low_list) * 100

    stock_data['KDJ_K'] = pd.ewma(rsv, com=2)
    stock_data['KDJ_D'] = pd.ewma(stock_data['KDJ_K'], com=2)
    stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
    #j=jin s=si c=cha, pinyin
    stock_data['KDJ_js'] = ''
    kdj_position = stock_data['KDJ_K'] > stock_data['KDJ_D']
    #note: the kdj_positon is a Series object not a common object, here use the bool filter use case 
    stock_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_js'] = 'jc'
    stock_data.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_js'] = 'sc'

    jc_stock_data = stock_data[(stock_data['KDJ_js'] == 'jc')]
    sc_stock_data = stock_data[(stock_data['KDJ_js'] == 'sc')]

    if jc_stock_data.empty:
        continue
    if sc_stock_data.empty:
	continue
    
    if jc_stock_data.shape[0] > sc_stock_data.shape[0]:
        jc_stock_data = jc_stock_data[:-1]  #delete the last jc
    elif jc_stock_data.shape[0] < sc_stock_data.shape[0]:
	sc_stock_data = sc_stock_data[1:]   #delete the first sc
    else:
	if jc_stock_data[0:1].index < sc_stock_data[0:1].index:
            jc_stock_data = jc_stock_data[:-1]
            sc_stock_data = sc_stock_data[1:]
    if jc_stock_data.shape[0] != sc_stock_data.shape[0]:
	print "Total jc number != total sc number"
	raise
    jc_stock_data = jc_stock_data.set_index(np.arange(jc_stock_data.shape[0]))
    sc_stock_data = sc_stock_data.set_index(np.arange(sc_stock_data.shape[0]))
    change_ratio = sc_stock_data.adjust_price / jc_stock_data.adjust_price - 1.0
    all_jc_sc_price_change_ratio = all_jc_sc_price_change_ratio.append(pd.DataFrame(change_ratio), ignore_index=True)

#print all_jc_sc_price_change_ratio 
#print all_jc_sc_price_change_ratio[all_jc_sc_price_change_ratio.adjust_price > 0]
print "The count number of kdj jincha&sicha in all the stocks of china is %d" % all_jc_sc_price_change_ratio.shape[0]
print
print "Rising probability is %.2f%%" % (all_jc_sc_price_change_ratio[all_jc_sc_price_change_ratio.adjust_price > 0].shape[0] / float(all_jc_sc_price_change_ratio.shape[0]) * 100)
print 
print "Rising scope is %s" % (all_jc_sc_price_change_ratio.mean() * 100)
print
