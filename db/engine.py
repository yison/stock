#!/opt/anaconda2/bin/python
from pymongo import MongoClient

_DB_CLIENT = None

def get_db_client():
    global _DB_CLIENT
    if _DB_CLIENT is None:
        print "None"
        _DB_CLIENT = MongoClient('10.239.131.155', 10001)
    return _DB_CLIENT 


