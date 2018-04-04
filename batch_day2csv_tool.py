import os
import sys
import csv
import gflags
from struct import *
from functools import partial

FLAGS = gflags.FLAGS

##TODO: put this in utils
def find_files(path, name_startswith):
    files = [(name, os.path.join(path, name)) for name in os.listdir(path)
             if os.path.isfile(os.path.join(path, name)) and name.startswith((name_startswith))]
    return files

def day2csv(input_file, output_file, csv_header):
    with open(output_file, 'w') as f_w:
        f_csv = csv.writer(f_w)
        f_csv.writerow(csv_header)
        with open(input_file, 'rb') as f:
            rows = []
            records = iter(partial(f.read, FLAGS.record_size), b'')
            for r in records:
                s_date, s_open, s_high, s_low, s_close, s_amount, s_vol, s_unknown = unpack('<LLLLLfLL', r)
                row = (s_date, s_open, s_high, s_low, s_close, int(s_amount), s_vol)
                rows.append(row)
        f_csv.writerows(rows)

def rename_file_type(file_name, old_file_type, new_file_type):
    return file_name.replace(old_file_type, new_file_type) 

def batch_day2csv(input_path, output_path, name_prefix, csv_header):
    files = find_files(input_path, name_prefix)
    for _file in files:
        file_name = _file[0]
        input_file = _file[1]
        new_file_name = rename_file_type(file_name, '.day', '.csv')
        output_file = os.path.join(output_path, new_file_name)
        day2csv(input_file, output_file, csv_header)

if __name__=="__main__":
    FLAGS(sys.argv)
    csv_header = ['date', 'open', 'high', 'low', 'close', 'amount', 'vol']
    input_path = FLAGS.raw_day_path 
    output_path = FLAGS.history_day_path 
    stock_name_prefix = (FLAGS.sh_stock_prefix, 
                         FLAGS.sz_stock_prefix,
                         FLAGS.zxb_stock_prefix,
                         FLAGS.cyb_stock_prefix)

    print (stock_name_prefix)
    batch_day2csv(input_path, output_path, stock_name_prefix, csv_header)
