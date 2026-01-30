import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build 
# This scope means "read-only access to calendar"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_credentials():
    creds = None
    
    # Check if we already have a saved token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If no token or it's expired, log in again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Save the token so we don't have to log in every time
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds

def get_todays_events(creds):
    service = build("calendar", "v3", credentials=creds)
    
    # Get the start and end of today
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0).isoformat() + "Z"
    end_of_day = now.replace(hour=23, minute=59, second=59).isoformat() + "Z"
    
    # Call the Google Calendar API
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    
    events = events_result.get("items", [])
    return events

def main():
    creds = get_credentials()
    events = get_todays_events(creds)
    
    if not events:
        print("No events today.")
    else:
        print(f"Today's events ({len(events)}):\n")
        for event in events:
            # YOUR TASK: extract and print each event
            # Hint: print the whole event first to see its structure
            print(event)
            print()  # blank line between events

if __name__ == "__main__":
    main()