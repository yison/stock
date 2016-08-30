#!/opt/anaconda2/bin/python
import datetime

def init_list(item, length):
    temp_list = []
    for i in range(length):
        temp_list.append(item)
    return temp_list 

def format_time(org_time, input_format="%Y%m%d", output_format="%Y-%m-%d"):
    time_array = time.strptime(org_time, input_format)
    return time.strftime(output_format, time_array)

def get_delta_dates(start, end):
    ##date format:i.e. 20161010
    start_date = datetime.datetime(int(start[0:4]), int(start[4:6]), int(start[6:8]))
    end_date = datetime.datetime(int(end[0:4]), int(end[4:6]), int(end[6:8]))
    delta = datetime.timedelta(days=1)
    delta_list = [int(start)]
    temp_date = start_date
    while True:
        if temp_date < end_date:
            temp_date = temp_date + delta * 1 
            delta_list.append(int(temp_date.strftime('%Y%m%d')))
        else:
            break
    print delta_list
    return delta_list
