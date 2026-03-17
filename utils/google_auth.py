import os
import sys
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar"
]

def get_google_credentials():
    # Construct paths relative to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    creds_path = os.path.join(base_dir, 'credentials.json')
    token_path = os.path.join(base_dir, 'token.json')

    creds = None
    
    # Priority 1: Check environment variable (Best for Render/Public Clouds)
    token_b64 = os.getenv("GOOGLE_TOKEN_BASE64")
    if token_b64:
        try:
            print("DEBUG AUTH: Found GOOGLE_TOKEN_BASE64 environment variable. Decoding...")
            token_data = json.loads(base64.b64decode(token_b64).decode('utf-8'))
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            print("DEBUG AUTH: Token loaded from environment variable.")
        except Exception as e:
            print(f"DEBUG AUTH: FAILED to load token from environment variable: {e}")

    # Priority 2: Check token.json file
    if not creds and os.path.exists(token_path):
        try:
            print(f"DEBUG AUTH: token.json found at {token_path}, loading...")
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            print(f"DEBUG AUTH: FAILED to load token.json: {e}")

    if not creds:
        print("DEBUG AUTH: No token found in environment or file.")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("DEBUG AUTH: Token expired, refreshing with refresh_token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"DEBUG AUTH: REFRESH FAILED: {e}. Falling back to new login flow.")
                creds = None # Force re-auth if refresh fails
        
        if not creds or not creds.valid:
            print("DEBUG AUTH: No valid token or refresh token. Attempting new login flow...")
            if not os.path.exists(creds_path):
                print(f"DEBUG AUTH: ERROR - credentials.json missing at {creds_path}")
                raise FileNotFoundError(f"Critical: {creds_path} not found. Please upload it to Render as a Secret File.")
            
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            
            try:
                print("DEBUG AUTH: Starting local server for auth (Expected to fail on Render if no token provided)...")
                creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
                
                # Save the new token locally for easier development
                print(f"DEBUG AUTH: Saving new token to {token_path}")
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"DEBUG AUTH: FAILED to run local server: {e}")
                raise RuntimeError(f"Authentication failed: {e}. Ensure token.json or GOOGLE_TOKEN_BASE64 is provided.")

    print("DEBUG AUTH: Credentials validated successfully.")
    return creds
