import base64
from email.mime.text import MIMEText
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
mcp = FastMCP("Gmail")

def get_gmail_service():
    creds = get_google_credentials()
    service = build("gmail", "v1", credentials=creds)
    return service

@mcp.tool()
def send_email(to: str, subject: str, message: str) -> str:
    """Send an email using Gmail."""
    service = get_gmail_service()

    msg = MIMEText(message)
    msg["to"] = to
    msg["subject"] = subject

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    body = {"raw": raw}

    service.users().messages().send(
        userId="me",
        body=body
    ).execute()

    return "Email sent successfully."

if __name__ == "__main__":
    mcp.run()