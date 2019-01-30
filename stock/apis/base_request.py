# coding:utf8
import aiohttp
import asyncio
import async_timeout
import json
import random
import warnings
import easyutils
import yarl
import time
import gflags

from stock import flags

FLAGS = gflags.FLAGS

class BaseRequest:
    def __init__(self):
        self._session = None
        self._proxy = FLAGS.proxy if FLAGS.proxy else None
        self._accept_encoding = "gzip, deflate, sdch"
        self._user_agents = [
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
        ]

    def __del__(self):
        if self._session is not None:
            self._session.close()

    def _get_user_agent(self):
        return random.choice(self._user_agents)

    def _get_headers(self):
        return {
                'User-Agent': self._get_user_agent(),
                'Accept-Encoding': self._accept_encoding 
                }

    async def get(self, url=None, url_type=None, timeout=0, sleep_time=0, res_type="json"):
        headers = self._get_headers()
        if self._session is None:
            self._session = aiohttp.ClientSession()
        attempt = 5
        while (attempt > 0):
            try:
                if sleep_time > 0:
                    time.sleep(sleep_time)
                with async_timeout.timeout(timeout):
                    async with self._session.get(url,
                                                 headers=headers,
                                                 proxy=self._proxy) as r:
                        status = r.status
                        data = await r.text()
                        res_data = None
                        if (200 == status):
                            if ("json" == res_type):
                                res_data = json.loads(data)

                            if (FLAGS.suf_stock_id == url_type):
                                stock_id = url.rsplit('/', maxsplit=1)[1]
                                return { stock_id: res_data }
                            else:
                                return res_data 
                        else:
                            print ({status:url})
                            return None
            except Exception as e:
                print ({e:url})
                attempt = attempt -1
                continue

    def get_data(self, url, url_type=None, timeout=100, sleep_time=0, res_type="json"):
        coroutine = self.get(url, url_type, timeout, sleep_time, res_type)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        res = loop.run_until_complete(coroutine)
        return res

    def get_urls_data(self, urls, url_type=None, timeout=0, sleep_time=0, res_type="json"):
        coroutines = []
        for url in urls:
            coroutine = self.get(url, url_type, timeout, sleep_time, res_type)
            coroutines.append(coroutine)
            coroutines.append(asyncio.sleep(0.25))
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        res = loop.run_until_complete(asyncio.gather(*coroutines))
        return res

    #async def get_stocks_by_range(self, params):
    #    if self._session is None:
    #        self._session = aiohttp.ClientSession()
    #    headers = {
    #        'Accept-Encoding': 'gzip, deflate, sdch',
    #        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
    #    }
    #    url = yarl.URL(self.stock_api + params, encoded=True)
    #    try:
    #        async with self._session.get(url, proxy=self.proxy, timeout=10, headers=headers) as r:
    #            response_text = await r.text()
    #            return response_text
    #    except asyncio.TimeoutError:
    #        return None

    #def get_stock_data(self, stock_list, **kwargs):
    #    coroutines = []

    #    for params in stock_list:
    #        coroutine = self.get_stocks_by_range(params)
    #        coroutines.append(coroutine)
    #    try:
    #        loop = asyncio.get_event_loop()
    #    except RuntimeError:
    #        loop = asyncio.new_event_loop()
    #        asyncio.set_event_loop(loop)
    #    res = loop.run_until_complete(asyncio.gather(*coroutines))

    #    return self.format_response_data([x for x in res if x is not None], **kwargs)

    #def format_response_data(self, rep_data, **kwargs):
    #    pass
