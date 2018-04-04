#!/bin/bash

#mongoimport --host=localhost --port=27017 --db stocks --collection base --type csv --headerline --file /root/mygithub/stock/data/stocks

DIR="/home/cloud001/ly/mygithub/stock/data/history/day"
HOST="10.239.131.215"
PORT="27017"
DATABASE="secondMarket"
TYPE="csv"

cd $DIR
csv_file=`ls`
#IFS=' ' 
for file in $csv_file
do 
    FILENAME=`echo $file | cut -b 3-8`
    echo $FILENAME
    mongoimport --host=$HOST --port=$PORT --db $DATABASE --collection $FILENAME --type $TYPE --headerline --file $DIR/$file
    #sleep 2
done
#mongoimport --host=localhost --port=27017 --db stocks --collection {} --type csv --headerline --file /root/mygithub/stock/data/history/{}
