import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar"
]

def get_google_credentials():
    # Construct paths relative to the project root
    # mcp_servers/ are at the same level as utils/
    # If called from a server script in mcp_servers/, base_dir is root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    creds_path = os.path.join(base_dir, 'credentials.json')
    token_path = os.path.join(base_dir, 'token.json')

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Critical: {creds_path} not found. Please upload it to Render as a Secret File.")
            
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            
            # Use run_local_server only if we have a display/browser (local mode)
            # On Render, this will fail and throw an error
            try:
                # access_type='offline' ensures we get a refresh token
                # prompt='consent' forces the refresh token to be sent if the user has already authed
                creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
            except Exception as e:
                raise RuntimeError(f"Authentication failed: {e}. Ensure token.json is provided.")
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds
