import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

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

source_data = youtubeAnalytics.reports().query(
    filters='video==tKrUu18hB58',
    metrics='audienceWatchRatio',
    dimensions='elapsedVideoTimeRatio'
)

# Pandas処理
df = pd.DataFrame(source_data)
# # 各動画毎に一意のvideoIdを取得
# df1 = pd.DataFrame(list(df['id']))['videoId']
# # 各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
# df2 = pd.DataFrame(list(df['snippet']))[['channelTitle', 'publishedAt', 'channelId', 'title', 'description']]
#
# ddf = pd.concat([df1, df2], axis=1)
#
#
# # 出力
# ddf.to_csv('output.csv')
print('出力完了')
print(df)
