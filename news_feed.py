#!/usr/bin/env python
import urllib , json 
import smtplib , sys , logging , ConfigParser , sched , time , os

s = sched.scheduler(time.time, time.sleep)

def get_config_data(section , attribute):
	try:
		config = ConfigParser.RawConfigParser()
		config.read('conf')
		data = config.get(section, attribute)
	except ConfigParser.Error as e:
		log_error("Error occurred while parsing configuration file. " + str(e))
	except:
		log_error("Unknown error occurred at get_config_data. " + sys.exc_info()[0])
	return data

def send_email(message , receivers):
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.ehlo()
		server.login(get_config_data('Credentials','username'),get_config_data('Credentials','password'))
		server.sendmail(get_config_data('Sender','email'),receivers,message)
		server.close()
	except smtplib.SMTPException as e:
		log_error("SMTP error occured at send_email. " + str(e) )
	except:
		log_error("Unknown error occurred at send_email" + sys.exc_info()[0])

def email_error(error):
	admins = get_config_data('Administrator','emails')
	sender = get_config_data('Sender','email')
	message = "\r\n".join([
		"From: " + sender,
		"To: " + admins,
		"Subject: Python Script Stopped",
		"",
		"Dear user, \n\n" 
		+ "Your python script used to update you about the hacker news top story suddenly stopped."
		+ "Error occeured was " + error
	])
	send_email(message , admins)

def email_top_story(top_story):
	users = get_config_data('Subscribers', 'emails') 
	message = "\r\n".join([
		"From: " + get_config_data('Sender','email'),
		"To: " + users,
		"Subject: Top News Changed: " + str(top_story['title'].encode("utf-8")),
		"",
		"Dear user, \n\n" 
		+ "\"" + str(top_story['title'].encode("utf-8")) + "\" is the top news at this moment on " + get_config_data('Site','url') + ".\n\n"
		+ "This news was reported by " + str(top_story['by'].encode("utf-8")) + " and has scored " + str(top_story['score']) + " points by now.\n\n"
		+ "Visit " + str(top_story['url']) + " to read more about this news.\n\nCheers..."
	])
	send_email(message , users)

def log_error(error):
	try:
		logging.basicConfig(filename='error.log' , format='%(asctime)s %(levelname)s %(message)s' , datefmt='%m/%d/%Y %I:%M:%S %p')
		logging.error(error)
	except IOError as e:
		email_error("I/O error({0}): {1}".format(e.errno, e.strerror) + error)
	except:
		email_error("Unknown error occurred at log_error. " + sys.exc_info()[0] + error)

def save_top_story(top_story):
	try:
		file = open('top_story' , 'w')
		file.write(str(top_story) + '\n')
		file.close()
	except IOError as e:
		log_error("I/O error({0}): {1}".format(e.errno , e.strerror))
	except:
		log_error("Unknown error at save_top_story. " + sys.exc_info()[0])

def read_last_top_story():
	try:
		if os.path.exists('top_story'):
			file = open('top_story' , 'r')
			last_top_story = file.readline()
			file.close()
		else:
			return ''
	except IOError as e:
		log_error("I/O error({0}): {1}".format(e.errno , e.strerror))
	except:
		log_error("Unknown error at read_last_top_story. " + sys.exc_info()[0])
	return last_top_story

def get_top_story(top_story_id):
	try :
		url = 'https://hacker-news.firebaseio.com/v0/item/' + str(top_story_id) + '.json'
		response = urllib.urlopen(url);
		return json.loads(response.read())
	except IOError as e:
		log_error("I/O error({0}): {1}".format(e.errno , e.strerror))
	except:
		log_error("Unknown error at get_top_story. " + sys.exc_info()[0])

def get_latest_top_stories():
	try :
		url = "https://hacker-news.firebaseio.com/v0/topstories.json"
		response = urllib.urlopen(url);
		top_stories = json.loads(response.read())
	except IOError as e:
		log_error("I/O error({0}): {1}".format(e.errno , e.strerror))
	except:
		log_error("Unknown error at get_latest_top_stories. " + sys.exc_info()[0])
	return top_stories
	
def main():
	duration =  (int(get_config_data('Duration','days')) * 24 * 60 * 60) + (int(get_config_data('Duration','hours')) * 60 * 60) + (int(get_config_data('Duration','minutes')) * 60) + int(get_config_data('Duration','seconds'))
	s.enter(10,1,main,())
	
	latest_top_stories = get_latest_top_stories()
	last_top_story = read_last_top_story()
	
	if(last_top_story == '' or int(last_top_story) != latest_top_stories[0]):
		top_story = get_top_story(latest_top_stories[0])
		email_top_story(top_story)
		save_top_story(top_story['id'])

def update_news_feed():
	s.enter(0,1,main,())
	s.run()

update_news_feed()
