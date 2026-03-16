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

def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
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