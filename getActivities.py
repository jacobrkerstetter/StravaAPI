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
import json

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
access_token = 'f27c8d4851826d4081f62d42805c47bf1468110e'
activity_data = []

# This list can be expanded
# @see https://developers.strava.com/docs/uploads/#upload-an-activity
# @see https://github.com/hozn/stravalib/blob/master/stravalib/model.py#L723

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

def create_new_activity(activity):
	new_activity = {
		'name' : activity.name,
		'distance' : str(meters_to_miles(activity.distance)) + ' mi.',
		'time' : str(format_time(activity.elapsed_time)),
		'heartrate' : 'not implemented',
		'kudos' : '0',
		'pace' : '0'
	}

	activity_data.append(new_activity)

def export_json():
	with open(os.path.join('StravaWidget', 'StravaWidgetExtension', 'userdata.json'), 'w') as _f:
		json.dump(activity_data, _f, indent=4)

def meters_to_miles(meters):
	return round(float(meters) * (1/1609.344), 2)

def format_time(time):
	strTime = str(time)
	if strTime[0] == '0':
		return strTime[2:]
	
	return strTime

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
	client.get_athlete()
	for i in range(2):
		try:
			athlete = client.get_athlete()
		except:
			if i > 0:
				logger.error("Daily Rate limit exceeded - exiting program")
				exit(1)
			logger.warning("Rate limit exceeded in connecting - Retrying strava connection in 15 minutes")
			time.sleep(900)
			continue
		break

	logger.info("Now authenticated for " + athlete.firstname + " " + athlete.lastname)

	# get latest run activity
	while True:
		activities = client.get_activities(limit=10)
		for activity in activities:
			if activity.type == 'Run':
				create_new_activity(activity)
				break
			
		export_json()
		time.sleep(360)

if __name__ == '__main__':
	main()