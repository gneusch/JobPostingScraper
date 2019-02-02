#!/bin/bash

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games"

DATE=`date +%Y_%m_%d`
FILENAME="$DATE"_indeed_uk.jl
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )/"
DATADIR="data/"
FILE=$SCRIPTDIR$DATADIR$FILENAME

while ! [ -s $FILE ]; do

	STIME=`date +%T` 
	echo "Scraping started for $DATE $STIME... filename: $FILE"
	(cd $SCRIPTDIR ; scrapy crawl IndeedUk -o "$DATADIR$FILENAME")

	if ! [ -s $FILE ]; then
		echo "File $FILE doesn't exist or empty, will retry in 5m..."
		sleep 5m
	fi
done
ETIME=`date +%T`
echo "Scraping finished for $DATE $ETIME..."
