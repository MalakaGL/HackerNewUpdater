#!/bin/bash
nohup python news_feed.py > /dev/null 2>&1 & echo $! > running_pid
while true;
do
	echo "Scheduler started..."
	./git_pull.sh
	echo "Scheduler sleeping..."
	sleep 20 
done
