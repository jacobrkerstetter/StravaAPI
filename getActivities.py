#!/usr/bin/env python

import os
from stravalib import Client, exc
from stravalib.util.limiter import RateLimiter, XRateLimitRule
from requests.exceptions import ConnectionError
import csv
import shutil
import time
from datetime import datetime, timedelta
import logging
import sys

logger = None

#####################################
# Access Token
#
# You need to run the strava_local_client.py script, with your application's ID and secret,
# to generate the access token.
#
# When you have the access token, you can
#   (a) set an environment variable `STRAVA_UPLOADER_TOKEN` or;
#   (b) replace `None` below with the token in quote marks, e.g. access_token = 'token'
#####################################
access_token = '616803c4b00ec2a5e3c48b52dedaf9f1853eb754'

cardio_file = 'cardioActivities.csv'

archive_dir = 'archive'
skip_dir = 'skipped'

# This list can be expanded
# @see https://developers.strava.com/docs/uploads/#upload-an-activity
# @see https://github.com/hozn/stravalib/blob/master/stravalib/model.py#L723
activity_translations = {
	'running': 'run',
	'cycling': 'ride',
	'mountain biking': 'ride',
	'hiking': 'hike',
	'walking': 'walk',
	'swimming': 'swim'
}

def set_up_logger():
	global logger
	logger = logging.getLogger(__name__)
	formatter = logging.Formatter('[%(asctime)s] [%(levelname)s]:%(message)s')
	std_out_handler = logging.StreamHandler(sys.stdout)
	std_out_handler.setLevel(logging.DEBUG)
	std_out_handler.setFormatter(formatter)
	file_handler = logging.FileHandler('strava-uploader.log')
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.addHandler(std_out_handler)
	logger.setLevel(logging.DEBUG)

def get_strava_access_token():
	global access_token

	if access_token is not None:
		logger.info('Found access token')
		return access_token

	access_token = os.environ.get('STRAVA_UPLOADER_TOKEN')
	if access_token is not None:
		logger.info('Found access token')
		return access_token

	logger.error('Access token not found. Please set the env variable STRAVA_UPLOADER_TOKEN')
	exit(1)

def get_strava_client():
	token = get_strava_access_token()
	rate_limiter = RateLimiter()
	rate_limiter.rules.append(XRateLimitRule(
			{'short': {'usageFieldIndex': 0, 'usage': 0,
						 # 60s * 15 = 15 min
						 'limit': 100, 'time': (60*15),
						 'lastExceeded': None,},
			 'long': {'usageFieldIndex': 1, 'usage': 0,
						# 60s * 60m * 24 = 1 day
						'limit': 1000, 'time': (60*60*24),
						'lastExceeded': None}}))
	client = Client(rate_limiter=rate_limiter)
	client.access_token = token
	return client

# Function to convert the HH:MM:SS in the Runkeeper CSV to seconds
def duration_calc(duration):
	# Splits the duration on the :, so we wind up with a 3-part array
	split_duration = str(duration).split(":")
	# If the array only has 2 elements, we know the activity was less than an hour
	if len(split_duration) == 2:
		hours = 0
		minutes = int(split_duration[0])
		seconds = int(split_duration[1])
	else:
		hours = int(split_duration[0])
		minutes = int(split_duration[1])
		seconds = int(split_duration[2])

	total_seconds = seconds + (minutes*60) + (hours*60*60)
	return total_seconds

# Translate RunKeeper's activity codes to Strava's
def activity_translator(rk_type):
	# Normalise to lower case
	rk_type = rk_type.lower()

	if rk_type not in activity_translations:
		return None

	return activity_translations[rk_type]

def increment_activity_counter(counter):
	counter += 1
	return counter

# designates part of day for name assignment, matching Strava convention for GPS activities
def strava_day_converstion(hour_of_day):
	if 3 <= hour_of_day <= 11:
		return "Morning"
	elif 12 <= hour_of_day <= 4:
		return "Afternoon"
	elif 5 <= hour_of_day <=7:
		return "Evening"

	return "Night"

# Get a small range of time. Note runkeeper does not maintain timezone
# in the CSV, so we must get about 12 hours earlier and later to account
# for potential miss due to UTC
def get_date_range(time, hourBuffer=12):
	if type(time) is not datetime:
		raise TypeError('time arg must be a datetime, not a %s' % type(time))


	return {
		'from': time + timedelta(hours = -1 * hourBuffer),
		'to': time + timedelta(hours = hourBuffer),
	}

def activity_exists(client, activity_name, start_time):
	date_range = get_date_range(start_time)

	logger.debug("Getting existing activities from [" + date_range['from'].isoformat() + "] to [" + date_range['to'].isoformat() + "]")

	activities = client.get_activities(
		before = date_range['to'],
		after = date_range['from']
	)

	for activity in activities:
		if activity.name == activity_name:
			return True

	return False

def miles_to_meters(miles):
	return float(miles) * 1609.344

def km_to_meters(km):
	return float(km) * 1000

def sec_to_min(sec):
	return float(sec) / 60

def m_per_s_to_min_per_mile(pace):
	# if activity is not running, return 0 pace
	if pace == 0:
		return 0
	
	# calculate min per mile with whole number seconds
	min_per_mile = 1 / (float(pace) * 60 * 0.001 * (1/1.609344))
	min = int(min_per_mile)
	sec = round((min_per_mile - min) * 60)

	return str(min) + ':' + str(sec) + ' / mile'

def main():
	set_up_logger()

	client = get_strava_client()

	logger.debug('Connecting to Strava')
	for i in range(2):
		try:
			athlete = client.get_athlete()
		except exc.RateLimitExceeded as err:
			if i > 0:
				logger.error("Daily Rate limit exceeded - exiting program")
				exit(1)
			logger.warning("Rate limit exceeded in connecting - Retrying strava connection in 15 minutes")
			time.sleep(900)
			continue
		break

	logger.info("Now authenticated for " + athlete.firstname + " " + athlete.lastname)

	activities = client.get_activities(limit=5)
	for activity in activities:
		if activity.sport_type == 'Run':
			pace = m_per_s_to_min_per_mile(activity.average_speed)
			print('{}: {}'.format(activity.name, pace))

if __name__ == '__main__':
	main()