import pickle
import os.path
import json
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from decouple import config
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def gsheet_api_check(SCOPES):
    creds = None
    try: 
        credsfile = json.loads(config('GOOGLE_CREDENTIALS'))
        with open('gcreds.json', 'w') as fp:
            json.dump(credsfile, fp)
        creds = service_account.Credentials.from_service_account_file("gcreds.json", scopes=SCOPES)
    except:
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                secret = json.loads(config('GOOGLE_CREDENTIALS_JSON'))
                flow = InstalledAppFlow.from_client_config(secret,SCOPES)
                # .from_client_secrets_file(
                #     'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
    return creds


def pull_sheet_data(SCOPES, SPREADSHEET_ID, RANGE_NAME):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=RANGE_NAME).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data


def get_transactions_dump(spreadsheet_id, tab_name):
    gsheet_api_check(SCOPES)
    data = pull_sheet_data(SCOPES, spreadsheet_id, tab_name)
    df = pd.DataFrame(data[1:], columns=data[0])
    return df
