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
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
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
