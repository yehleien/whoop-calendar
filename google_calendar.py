from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarClient:
    def __init__(self, credentials_path='credentials.json', token_path='token.pickle'):
        creds = None
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            # In CI, do not attempt interactive OAuth; require a valid token.pickle
            running_in_ci = os.getenv('CI') == '1'
            if creds and creds.expired and creds.refresh_token:
                # Try to refresh; if it fails in CI, raise a clear error
                try:
                    creds.refresh(Request())
                except Exception as exc:
                    if running_in_ci:
                        raise RuntimeError('Google token refresh failed in CI. Update GOOGLE_TOKEN secret (base64 of token.pickle) generated with the same credentials.json).') from exc
                    raise
            else:
                if running_in_ci:
                    raise RuntimeError('token.pickle not present/valid in CI. Provide GOOGLE_TOKEN secret (base64 of token.pickle).')
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=50034)
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('calendar', 'v3', credentials=creds)

    def add_event(self, calendar_id, event):
        return self.service.events().insert(calendarId=calendar_id, body=event).execute() 