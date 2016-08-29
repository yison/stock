#!/bin/bash

mongoimport --host=localhost --port=10001 --db stocks --collection base --type csv --headerline --file /root/mygithub/stock/data/stocks

directory="/root/mygithub/stock/data/history/"
cd $directory
csv_file=`ls`
#IFS=' ' 
for file in $csv_file
do 
    echo $file
    mongoimport --host=localhost --port=10001 --db stocks --collection $file --type csv --headerline --file /root/mygithub/stock/data/history/$file
    #sleep 2
done
#mongoimport --host=localhost --port=10001 --db stocks --collection {} --type csv --headerline --file /root/mygithub/stock/data/history/{}
