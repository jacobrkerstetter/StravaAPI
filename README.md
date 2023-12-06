# Strava to LED Matrix
The purpose of this project is to connect to the Strava API and display a recent activity to an LED Matrix

## Steps to authentication
The first steps of using the Strava API for any project is authentication. 

1. Set up Strava API account online and locate client ID and client secret
2. Run getAccess.py as follows: python getAccess.py <client_id> <client_secret>
    a. This will load a link to authenticate online via Strava. Once authenticate, copy the code returned
3. Paste the code into getActivities.py and run as follows: python3 getActivity.py