import os
import pandas as pd
import gflags
from stock import flags

from stock.apis.base_request import BaseRequest

FLAGS = gflags.FLAGS

class Eniu(BaseRequest):
    def __init__(self):
        super().__init__()
        self.domain = FLAGS.eniu_domain 
        self.pre_urls = [
            self.domain + "/static/data/stock_list.json",
            self.domain + "/chart/pea/",
            self.domain + "/chart/gethkpehistory/",
            self.domain + "/chart/getguindexpehistory/",
            self.domain + "/chart/pba/",
            self.domain + "/chart/gethkpbhistory/",
            self.domain + "/chart/getdvhistory/",
            self.domain + "/chart/getroe/",
            self.domain + "/chart/getmarketvaluehistory/",
        ]

    def get_stocks(self):
        stocks_url = self.pre_urls[0]
        res = self.get_data(stocks_url)
        return res

    def get_stock_ids(self):
        stocks = self.get_stocks()
        return [x['stock_id'] for x in stocks]

    def get_stock_ids_by_excluder(self, excluder="hk"):
        stocks = self.get_stocks()
        return [x['stock_id'] for x in stocks if excluder not in x['stock_id']]

    def get_stock_ids_by_filter(self, filter_factor="hk"):
        stocks = self.get_stocks()
        return [x['stock_id'] for x in stocks if filter_factor in x['stock_id']]

    def get_history(self, stock_ids, type_factor="pe"):
        pre_uri = self.pre_urls[1]
        path = "" 

        res_list = []
        for stock_id in stock_ids:
            if ("pe" == type_factor):
                path = os.path.join(FLAGS.pe_history_path, stock_id)

                if (FLAGS.hk_prefix in stock_id):
                    pre_uri = self.pre_urls[2]
                elif (FLAGS.index_prefix in stock_id):
                    pre_uri = self.pre_urls[3]

            elif ("pb" == type_factor):
                path = os.path.join(FLAGS.pb_history_path, stock_id)
                if (FLAGS.hk_prefix in stock_id):
                    pre_uri = self.pre_urls[5]
                else:
                    pre_uri = self.pre_urls[4]
            elif ("dv" == type_factor):
                pass
            elif ("roe" == type_factor):
                pass
            else:
                pass

            url = pre_uri + stock_id
            data = self.get_data(url,
                           url_type=FLAGS.suf_stock_id,
                           timeout=20,
                           sleep_time=1)

            if data:
                for key, value in data.items():
                        try:
                            df = pd.DataFrame(value)
                            df.to_csv(path)
                        except Exception as e:
                            print ({e: {stock_id:value}})
            else:
                res_list.append({stock_id:url})
        return res_list
        
    def get_pe_history(self):
        stock_ids = self.get_stock_ids()
        res = self.get_history(stock_ids, type_factor="pe")
        return res

    def get_pb_history(self):
        stock_ids = self.get_stock_ids()
        res = self.get_history(stock_ids, type_factor="pb")
        return res

    def get_dv_history(self):
        pass

    def get_roe_history(self):
        pass
