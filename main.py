import requests
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["APP_KEY"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
WORKOUT_TOKEN = os.environ["WORKOUT_TOKEN"]

workout_endpoint = f'https://api.sheety.co/{SPREADSHEET_ID}/workoutTracking/workouts'

exercise = input('Tell me which exercises you did: ')
exercise_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
headers = {
    'Content-Type': 'application/json',
    'x-app-id': APP_ID,
    'x-app-key': API_KEY
}

body = {
    "query": exercise
}

response = requests.post(exercise_endpoint, json=body, headers=headers)
exercises = response.json()['exercises']
today = datetime.now()

for exercise in exercises:
    bearer_headers = {
        "Authorization": f'Bearer {WORKOUT_TOKEN}'
    }

    body = {
        'workout': {
            'date': today.strftime('%m/%d/%Y'),
            'time': today.strftime('%H:%M:%S'),
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }

    response = requests.post(workout_endpoint, json=body, headers=bearer_headers)
    response.raise_for_status()
