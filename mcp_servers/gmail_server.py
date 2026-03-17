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
    # Construct paths relative to the project root (one level up from this script in mcp_servers/)
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
            # This will still fail on Render, but we provide a better error message now
            try:
                creds = flow.run_local_server(port=0)
            except Exception as e:
                raise RuntimeError(f"Authenticating failed: {e}. Ensure token.json is uploaded as a Secret File on Render.")
        
        with open(token_path, 'w') as token:
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