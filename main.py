import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'credentials/client_id.json'
CLIENT_PICKLE_FILE = 'credentials/token.pickle'

# Authentication
creds = None
if os.path.exists(CLIENT_PICKLE_FILE):
    with open(CLIENT_PICKLE_FILE, 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(CLIENT_PICKLE_FILE, 'wb') as token:
        pickle.dump(creds, token)

# Youtube API
youtubeAnalytics = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

response = youtubeAnalytics.reports().query(
    ids='channel==MINE',
    startDate='2020-09-02',
    endDate='2020-12-14',
    filters='video==tKrUu18hB58',
    metrics='audienceWatchRatio',
    dimensions='elapsedVideoTimeRatio'
).execute()

# Pandas処理
headers = pd.DataFrame(response['columnHeaders'])
data = pd.DataFrame(response['rows'], columns=headers['name'])

# グラフ
plt.figure()
data.plot(x='elapsedVideoTimeRatio')
plt.savefig('output/graph.png')
plt.close('all')

# データ
data.to_csv('output/data.csv')

print('出力完了')
print(data)
