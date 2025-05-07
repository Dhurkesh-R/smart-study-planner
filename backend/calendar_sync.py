import datetime
import os.path
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging to file and console
logger = logging.getLogger('calendar_logger')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('calendar_integration.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google():
    """Handles Google OAuth2 authentication."""
    creds = None
    try:
        if os.path.exists('../integrations/token.json'):
            creds = Credentials.from_authorized_user_file('../integrations/token.json', SCOPES)
            logger.info("Loaded credentials from ../integrations/token.json.")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logger.info("Refreshed expired credentials.")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../integrations/credentials.json', SCOPES
                )
                creds = flow.run_local_server(port=0)
                logger.info("Completed new OAuth2 flow.")

            with open('../integrations/token.json', 'w') as token:
                token.write(creds.to_json())
                logger.info("Saved new credentials to ../integrations/token.json.")

    except Exception as e:
        logger.error(f"Google authentication failed: {e}", exc_info=True)
        raise RuntimeError(f"Google authentication failed: {e}")

    return creds

def create_study_event(subject: str, start_time: str, duration_minutes: int = 60):
    """
    Creates a study session event on Google Calendar.
    - start_time: ISO 8601 format (e.g., '2025-05-07T15:00:00')
    """
    try:
        creds = authenticate_google()
        service = build('calendar', 'v3', credentials=creds)

        start = datetime.datetime.fromisoformat(start_time)
        end = start + datetime.timedelta(minutes=duration_minutes)

        event = {
            'summary': f'Study: {subject}',
            'description': f'Smart Study Planner session for {subject}.',
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': 'UTC',
            },
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        logger.info(f"Successfully created event for {subject} at {start_time}.")
        return f"✅ Event created: {created_event.get('htmlLink')}"

    except HttpError as http_err:
        logger.error(f"Google Calendar API error: {http_err}", exc_info=True)
        return f"❌ Google Calendar API error: {http_err}"

    except Exception as e:
        logger.error(f"Failed to create event: {e}", exc_info=True)
        return f"❌ Failed to create event: {e}"
