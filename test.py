import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

code = '27927279b501293cced4210a7f57e6edcc785d43'
info = {
    'client_id': '116316',
    'client_secret': '7b62a69c8df740a6d08be9a438b0999cb35ffab6',
    'code': code,
    'grant_type': 'authorization_code'
}

data = requests.post(auth_url, files=info)
print(data)

'''
header = {'Authorization': 'Bearer ' + "2a8176e61600a71dcc72aec813743ae5fd73c7f3"}
param = {'per_page': 200, 'page': 1}
data = requests.get(activites_url, headers=header, params=param).json()

print(data[2])
'''