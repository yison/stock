import csv
import redis
import json


def filter_data(stock_id, stock_directory):
    path = stock_directory + stock_id
    with open(path, 'rb') as local_file:
        reader = csv.DictReader(local_file)
        per_day_data_list = []
        for row in reader:
            if "000" == row['Volume']:
                continue
            else:
                per_day_data_list.append(row)
        return per_day_data_list


if __name__ == "__main__":
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    db = redis.StrictRedis(connection_pool=pool)
    value = filter_data('603998', '/home/hadoop/ly/')
    json_value = json.dumps(value)
    db.set('603998', json_value)
