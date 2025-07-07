#!/usr/bin/env python3
"""
Test sync with mock Whoop API
"""

from mock_whoop import MockWhoopAPIClient, load_whoop_token
from google_calendar import GoogleCalendarClient
import json
import os
from datetime import datetime, timedelta

GOOGLE_CALENDAR_ID = 'primary'
SYNCED_FILE = 'synced_workouts.json'

def load_synced_ids():
    if os.path.exists(SYNCED_FILE):
        with open(SYNCED_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_synced_ids(ids):
    with open(SYNCED_FILE, 'w') as f:
        json.dump(list(ids), f)

def workout_to_event(workout):
    start = datetime.fromisoformat(workout['start']).isoformat()
    end = datetime.fromisoformat(workout['end']).isoformat()
    return {
        'summary': f"Whoop Workout: {workout.get('sport', 'Workout')}",
        'description': f"Whoop workout ID: {workout['id']}\nDuration: {workout.get('duration', 0)//60} minutes\nStrain: {workout.get('strain', 0)}\nCalories: {workout.get('calories', 0)}",
        'start': {'dateTime': start, 'timeZone': 'UTC'},
        'end': {'dateTime': end, 'timeZone': 'UTC'},
    }

def sync_mock():
    """Sync mock workouts to Google Calendar"""
    print("Testing sync with mock Whoop data...")
    
    whoop = MockWhoopAPIClient("mock_token")
    gcal = GoogleCalendarClient()
    synced_ids = load_synced_ids()
    
    workouts = whoop.get_workouts()
    new_ids = set()
    
    for workout in workouts:
        if workout['id'] not in synced_ids:
            event = workout_to_event(workout)
            try:
                gcal.add_event(GOOGLE_CALENDAR_ID, event)
                new_ids.add(workout['id'])
                print(f"✅ Added workout: {workout.get('sport', 'Workout')} on {workout['start']}")
            except Exception as e:
                print(f"❌ Failed to add workout: {e}")
        else:
            print(f"⏭️  Skipped workout: {workout.get('sport', 'Workout')} on {workout['start']} (already synced)")
    
    save_synced_ids(synced_ids.union(new_ids))
    print(f"🎉 Synced {len(new_ids)} new workouts to Google Calendar!")

if __name__ == '__main__':
    sync_mock() 