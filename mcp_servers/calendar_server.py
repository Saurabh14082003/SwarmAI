from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Calendar")

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
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
