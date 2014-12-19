#!/bin/zsh
echo "git pull started..."

if [[ ! -z  $(git status --short | grep '^?') ]] ; then
	echo "Untracked files are available"
	exit 1
fi

if [[ ! -z  $(git status --short | grep '^ ') ]] ; then
	echo "Changes are available which are not added."
	exit 1
fi

if [[ ! -z  $(git status --short | grep '^M') ]] ; then
	echo "Uncommitted changes are available which are added."
	exit 1
fi

branch=$(git branch | grep '*' | sed -e 's/^\* \(.*\)$/\1/')

if [ "$branch" != "master" ] ; then
	echo "Current branch is not master."
	exit 1
fi

hash=$(git rev-parse --short head)
git pull origin master
log=$(git log --pretty=format:"%H   %s" ORIG_HEAD..HEAD)

conf=$(git diff $hash conf_sample);

if [ "$conf" != "" ] ; then
	echo "**********************************************************"
	echo "**********Configuration file has changed.*****************"
	echo "**********************************************************"
fi

echo "Ready to kill last process..."
kill -9 $(<"running_pid")

echo "Running commit: $log" >> log_file
nohup python news_feed.py > /dev/null 2>&1 & echo $! > running_pid
echo "Cheking started..."
while [  $count -lt 3 ];
do
	pid=$(<"running_pid")
	echo "Process is $pid"
	if [[ -z $(ps -e | grep $pid) ]] ; then
		echo "Script stopped."
	else
		echo "Process running."
	fi
	count=$((count+1))
	sleep 5
done
echo "Script is running well..."
