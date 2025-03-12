import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import dotenv

config = dotenv.dotenv_values(".env")
# Set up your Strava credentials
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']

# Initialize FastAPI app
app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Step 1: Direct the user to authenticate with Strava
@app.get("/")
async def login(request: Request):
    auth_url = f'http://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=auto&scope=read_all'
    return RedirectResponse(auth_url)

# Step 2: Handle the OAuth callback
@app.get("/authorize")
async def authorize(request: Request, code: str):
    if not code:
        raise HTTPException(status_code=400, detail="No code received from Strava")

    # Step 3: Exchange authorization code for access token
    token_url = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
    }

    
    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Error: {response.status_code}, {response.text}")

    # Step 4: Extract the access token from the response
    data = response.json()
    access_token = data.get('access_token')
# Fetch and return activities
    activities = get_segments(access_token)

    segment = get_segment_efforts(access_token)

    return {"message": "Authentication successful!", "access_token": access_token, "activities": activities, "pr_attempt": segment}

# Function to fetch activities from Strava
def get_activities(access_token):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        activities = response.json()
        return activities
    else:
        return f"Error fetching activities: {response.status_code}, {response.text}"
    
def get_segments(access_token):
    url = 'https://www.strava.com/api/v3/segments/3615418'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        segments = response.json()
        return segments
    else:
        return f"Error fetching segments: {response.status_code}, {response.text}"
    
def get_segment_efforts(access_token):
    url = 'https://www.strava.com/api/v3/segment_efforts/13779291151'
    x = 13779291151
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        segments = response.json()
        return segments
    else:
        return f"Error fetching segments: {response.status_code}, {response.text}"
# To run the app:
# uvicorn your_script_name:app --reload
