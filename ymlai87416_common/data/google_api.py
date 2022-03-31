from __future__ import print_function

import os.path
import yaml
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import logging

# Google API
# Create an application in Google Cloud Platform to enable me to read google sheet in my drive.
# Please provide 2 things

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def read_spreadsheet(spreadsheet_id, range, config):
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.

    Parameters
    ----------
    spreadsheet_id : str
        Google spreadsheet id
    range : str
        Range to read
    config: dict
        configuration

    Returns
    -------
    values: multi-dimensional array
        the values from the spreadsheet
    """

    creds = None

    # use service_key if available
    if "google_service_key" in config:
        service_key = config["google_service_key"]

        if os.path.exists(service_key):
            creds = service_account.Credentials.from_service_account_file(service_key, scopes=SCOPES)
            if not creds is None: 
                logging.info("Successfully authenticate google sheet using service account.")
        
    if creds is None: 
        token_path = config["google_token_path"]
        credential_path = config["google_cred_path"]
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logging.info("Successfully authenticate google sheet using api key. (R)")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential_path, SCOPES)
                creds = flow.run_local_server(port=0)
                logging.info("Successfully authenticate google sheet using api key. (L)")
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range).execute()
        values = result.get('values', [])

        return values
        
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1JC5yyhtGaQTBSBEN1-LxF3-YlQM1HkIUO27U06_vUoM'
    SAMPLE_RANGE_NAME = 'crypto!A4:C'

    secret_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..","..", "secret.yaml")
    stream = open(secret_path, "r")
    data = yaml.safe_load(stream)

    values = read_spreadsheet(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME, data)

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        print(values)
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[2]))