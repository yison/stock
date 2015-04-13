from multiprocessing.dummy import Pool
import urllib2
import operator
import datetime
import time
import socket
import requests
import traceback


global exchange_url_map
exchange_url_map = {}


def get_stock_codes_by_pre(pre_stock_code):
    stock_code = []
    for i in range(1, 1000):
        stock_code.append(pre_stock_code + str(i).zfill(3))
    #print stock_code
    return stock_code


def stock_codes_of_exchange(pre_codes):
    return reduce(operator.add, map(get_stock_codes_by_pre, pre_codes))
    #return reduce(lambda x,y:x+y, map(get_stock_codes_by_pre, pre_codes))


def join_url(endpoint, exchange_code):
    base_url = 'http://table.finance.yahoo.com/table.csv?s='

    if "" == exchange_code:
        return base_url + endpoint
    else:
        return base_url + endpoint + "." + exchange_code


def get_urls_of_exchange(exchange):
    urls = []
    global exchange_url_map
    if 'ss' == exchange:
        pre_code = ['600', '601', '603']
        stock_list = stock_codes_of_exchange(pre_code)
    elif 'sz' == exchange:
        pre_code = ['000', '002']
        stock_list = stock_codes_of_exchange(pre_code)
    elif '' == exchange:
        pre_code = ['300']
        stock_list = stock_codes_of_exchange(pre_code)

    for x in stock_list:
        urls.append(join_url(x, exchange))
    exchange_url_map.update((dict(zip(urls, stock_list))))
    return urls


def download(url):
    while(True):
        ret = None
        try:
            ret = requests.get(url)
            if 200 == ret.status_code:
                with open('./stocks/%s' % exchange_url_map[url], 'wb') as fd:
                    fd.write(ret.text)  
                print "Download:%s" % exchange_url_map[url]
                break
            elif 404 == ret.status_code:
                print "404:url:%s" % (url)
                break
            elif 503 == ret.status_code:
                print "503:url:%s" % (url)
                continue
        except Exception, e:
            print "error happended!url:%s"  % (url)
            print Exception
            print e
            continue


if __name__ == "__main__":
    base_url = 'http://table.finance.yahoo.com/table.csv?s='
    exchanges =['ss', 'sz', ''] #Shanghai, Shenzhen, Chuangyeban

    all_urls = reduce(operator.add, map(get_urls_of_exchange, exchanges))
    #print all_urls
    #print exchange_url_map

    start_time = datetime.datetime.now()
    pool = Pool(10)
    #proxy = "proxy-shz.intel.com:911"
    #proxies = {"http":"http://%s" % proxy}
    #proxy_support = urllib2.ProxyHandler(proxies)
    #opener = urllib2.build_opener(proxy_support)
    #urllib2.install_opener(opener)
     
    ret_list  = pool.map(download, all_urls)
    pool.close()
    pool.join()
    end_time = datetime.datetime.now()
    print start_time
    print end_time 


