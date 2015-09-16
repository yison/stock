# -*- coding: utf-8 -*-
import os
import pandas as pd

stock_code_list = []
for root, dirs, files in os.walk('data/all_trading_data/stock_data'):
    if files:
        for f in files:
            if '.csv' in f:
                stock_code_list.append(f.split('.csv')[0])


all_stock = pd.DataFrame()

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
    # 
    #for n in [1, 2, 3, 5, 10, 20]:
    #    stock_data[str(n)+'_days_price_change_rario'] = stock_data['adjust_price'].shift(-1*n) / stock_data['adjust_price'] - 1.0
    #stock_data.dropna(how='any', inplace=True)#delete all the null data row

    stock_data = stock_data[(stock_data['KDJ_js'] == 'jc')]
    if stock_data.empty:
        continue
    all_stock = all_stock.append(stock_data, ignore_index=True)

print 
print "The count of kdj jincha in all the stocks of china is %d" % all_stock.shape[0]
print 

#for n in [1, 2, 3, 5, 10, 20]:
#    print "金叉之后的%d个交易日内，" % n,
#    print "平均涨幅为%.2f%%，" % (all_stock[str(n)+'_days_price_change_rario'].mean() * 100),
#    print "其中上涨股票的比例是%.2f%%。" % \
#          (all_stock[all_stock[str(n)+'_days_price_change_rario'] > 0].shape[0]/float(all_stock.shape[0]) * 100)
#    print
