import csv
import redis
import itertools


if __name__ == "__main__":
    with open('/home/hadoop/ly/603998', 'rb') as file:
        reader = csv.DictReader(file)
        per_day_data_list = []
        for row in reader:
            if "000" == row['Volume']:
                continue 
            else:
                per_day_data_list.append(row)
        print per_day_data_list[0]
        #chunks = itertools.groupby(reader, keyfunc)
        #print list(chunks)[0]
