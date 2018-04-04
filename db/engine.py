import gflags
from influxdb import InfluxDBClient
from influxdb import DataFrameClient 
from pymongo import MongoClient

FLAGS = gflags.FLAGS

def get_db_client(client=None):
    if client == FLAGS.influxdb_client:
        return InfluxDBClient(host='10.239.131.215', port=8086, retries=5)
        #_DB_CLIENT = DataFrameClient(host='10.239.131.157', port=8086, username='root', password='root')
    elif client == FLAGS.mongodb_client:
        return MongoClient('10.239.131.215', 27017)
    else:
        return None


