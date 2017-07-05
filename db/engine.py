#!/opt/anaconda2/bin/python
from pymongo import MongoClient
from influxdb import InfluxDBClient
from influxdb import DataFrameClient 

_DB_CLIENT = None

def get_db_client():
    global _DB_CLIENT
    if _DB_CLIENT is None:
        #TODO: use config
        #_DB_CLIENT = MongoClient('10.239.131.155', 10001)
        #_DB_CLIENT = InfluxDBClient(host='10.239.131.157', port=8086, database='history', retries=5) 
        _DB_CLIENT = DataFrameClient(host='10.239.131.157', port=8086, username='root', password='root') 
    return _DB_CLIENT 


