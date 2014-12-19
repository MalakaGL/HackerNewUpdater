#!/bin/zsh
count=0
echo "Cheking started..."
while [  $count -lt 3 ];
do
	pid=$(<"running_pid")
	echo "Process is $pid"
	if [[ -z $(ps -e | grep $pid) ]] ; then
		echo "Script stopped. Trying to restart."
		nohup python news_feed.py > /dev/null 2>&1 & echo $! > running_pid
		count=0
	else
		echo "Process running."
	fi
	count=$((count+1))
	sleep 5
done
