from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Calendar")

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def get_calendar_service():
    # Construct paths relative to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    creds_path = os.path.join(base_dir, 'credentials.json')
    token_path = os.path.join(base_dir, 'token.json')

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Critical: {creds_path} not found. Please upload it to Render as a Secret File.")

            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            try:
                creds = flow.run_local_server(port=0)
            except Exception as e:
                raise RuntimeError(f"Authenticating failed: {e}. Ensure token.json is uploaded as a Secret File on Render.")
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service

@mcp.tool()
def create_event(summary: str, start_time: str, duration_minutes: int = 30) -> str:
    """Create a calendar event."""
    service = get_calendar_service()

    start = datetime.fromisoformat(start_time)
    end = start + timedelta(minutes=duration_minutes)

    event = {
        "summary": summary,
        "start": {"dateTime": start.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end.isoformat(), "timeZone": "Asia/Kolkata"},
    }

    event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return f"Event created: {event.get('htmlLink')}"

if __name__ == "__main__":
    mcp.run()
