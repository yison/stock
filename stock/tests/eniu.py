# coding:utf8
import os
import sys
import gflags
from stock import flags
from stock import apis

import unittest

FLAGS = gflags.FLAGS

class TestEniu(unittest.TestCase):
    ## have to run testcase with "test_xxx"
    #def test_get_stock_list(self):
    #    api = apis.use(FLAGS.eniu)
    #    stocks = api.get_stock_list()
    #    with open('/tmp/output', 'w') as f:
    #        print (stocks, file=f) 
    #    return stocks


    def test_get_pe_history(self):
        api = apis.use(FLAGS.eniu)
        res = api.get_pe_history()
        return res 

    def test_get_pb_history(self):
        api = apis.use(FLAGS.eniu)
        res = api.get_pb_history()
        return res 

if __name__ == '__main__':
    FLAGS(sys.argv)
    unittest.main()
