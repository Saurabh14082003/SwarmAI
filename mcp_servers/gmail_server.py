import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Gmail")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar"
]

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def get_gmail_service():
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