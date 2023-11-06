import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "xxxx",
    'client_secret': 'xxxx',
    'refresh_token': 'xxxx',
    'grant_type': "refresh_token",
    'f': 'json'
}

header = {'Authorization': 'Bearer ' + "2a8176e61600a71dcc72aec813743ae5fd73c7f3"}
param = {'per_page': 200, 'page': 1}
data = requests.get(activites_url, headers=header, params=param).json()

print(data[2])