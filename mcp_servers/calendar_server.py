from datetime import datetime, timedelta
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP
import os
import sys

# Add project root to path so we can import utils
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.google_auth import get_google_credentials

# Initialize FastMCP server
mcp = FastMCP("Calendar")

def get_calendar_service():
    creds = get_google_credentials()
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
