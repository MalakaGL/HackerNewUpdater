
COPYRIGHT

HackerNewsFeed Version 1.0
Copyright      2014 - Allion Technologies(Interns) All rights reserved

LICENSE

This script is free software; you are free to redistribute it
and/or modify it under the same terms as Python itself.

URL

The most up to date version of this script is available 
at: https://github.com/MalakaGL/HackerNewUpdater

SUMMARY

HackerNewsUpdater is a Python based script which can be set to run on a server.
This script will check the top story at https://news.ycombinator.com exactly
once a given time duration.
When the top story is not the one which it was within the last check the 
script will send the updated top story details to all the subscribers.

FILES

In this distribution, you will find the following files:

news_feed.py                    - The main Python script
ReadMe.txt                      - This file. Instructions on how to install and use HackerNewsUpdater
conf-sample                     - Configuration file for the script

CONFIGURATION

There are a number of variables that you can change in HackerNewsUpdater which
alter the way that the program works.
All these variables are defined in conf file.
You have to save the given "conf-sample" such that all the variables are set to
correct values and save it as "conf".

[Credentials]		- These credentials will be used to log into a gmail account.
					  This email account will be used to send all the emails that
					  the script will send.
					
[Subscribers]		- This field will require a list of email addresses of the users 
					  who need to get updates from Hacke News.
					  
[Administrator]		- This field will hold a list of administrators who are going to be
					  responsible for the proper functionality of the script.
					  If the script failed to execute at some point an email will be sent
					  to these administrators including the error messages generated.

[Sender]			- This email will be displayed as the sender of all the emails sent by the script.

[Site]				- This is the site URL where these data is taken from.
					  This data is placed here to use in case of URL change of that site.
					  
[Duration]			- This defines the time interval between two executions of the script.
					  Time period can be defined in days, hours or seconds.
					  0 should be used to indicate null.
					  
INSTALLATION

Configure the "conf-sample"" file as you wish.
Save it as "conf" in the same directory where the "news_feed.py" is.
Run the "news_feed.py" using the command "python news_feed.py"

COMMON PROBLEMS

To be added.
:D

SUPPORT

For support of this script please email:

  glmalaka@gmail.com
