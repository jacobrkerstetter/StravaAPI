from stravalib.client import Client

client = Client()
CLIENT_ID, CLIENT_SECRET = open('client.secret').read().strip().split(',')

authorize_url = client.authorization_url(
    client_id=CLIENT_ID, redirect_uri='http://127.0.0.1:5000/authorization', scope=['read_all','profile:read_all','activity:read_all']
)
print(authorize_url)