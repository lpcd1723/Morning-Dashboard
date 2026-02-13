import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build 
from modules.cache import get_cached_data, save_to_cache
from modules.config import load_config

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


def get_todays_events():
   
    config = load_config()
    cache_time = config["calendar"]["cache_duration"]

    cached = get_cached_data("cache/calendar.json",cache_time)
    if cached:
        return cached

    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    
    # Get the start and end of today
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0).isoformat() + "Z"
    end_of_day = now.replace(hour=23, minute=59, second=59).isoformat() + "Z"
    
    calendar_ids = config["calendar"]["calendar_ids"]
    all_events = []

    for cal_id in calendar_ids:
        events_result = service.events().list(
            calendarId=cal_id,
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        for event in events_result.get("items", []):
            location = event.get("location", "")
            eventData = {
                "summary": event["summary"],
                "startTime": datetime.fromisoformat(event["start"]["dateTime"].replace("Z", "")).strftime("%H:%M"),
                "endTime": datetime.fromisoformat(event["end"]["dateTime"].replace("Z", "")).strftime("%H:%M"),
                "location": location
            }
            all_events.append(eventData)
            
    all_events.sort(key=lambda e: e["startTime"])
    
    if not all_events:
        data = {"eventNumber": 0, "events": [{"summary": "No events today.", "startTime": "", "endTime": "", "location": ""}]}
    else:
        data = {"eventNumber": len(all_events), "events": all_events}
    

    save_to_cache("cache/calendar.json",data)
    return data




