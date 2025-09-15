from whoop_api import WhoopAPIClient
from google_calendar import GoogleCalendarClient
import json
import os
from datetime import datetime, timedelta, timezone
import argparse
import requests

# Set this to your Exercise calendar's ID (from Google Calendar settings)
GOOGLE_CALENDAR_ID = '4539865cdc49ca859f905499096f1b799ea4224619459e0121c70acd59802cd0@group.calendar.google.com'  # Exercise calendar ID
SLEEP_CALENDAR_ID = 'ef057c084d263cb5b5c2af5a3698582afbb093ccfa9c599f651685986a3cbaa7@group.calendar.google.com'  # Sleep calendar ID
SYNCED_FILE = 'synced_workouts.json'
SYNCED_SLEEP_FILE = 'synced_sleep.json'

def load_whoop_token():
    """Load Whoop access token from file"""
    if os.path.exists('whoop_token.json'):
        with open('whoop_token.json', 'r') as f:
            token_data = json.load(f)
            return token_data['access_token']
    else:
        raise FileNotFoundError("whoop_token.json not found. Run get_token.py first to get your access token.")

def load_synced_ids():
    if os.path.exists(SYNCED_FILE):
        with open(SYNCED_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_synced_ids(ids):
    with open(SYNCED_FILE, 'w') as f:
        json.dump(list(ids), f)

def load_synced_sleep_ids():
    if os.path.exists(SYNCED_SLEEP_FILE):
        with open(SYNCED_SLEEP_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_synced_sleep_ids(ids):
    with open(SYNCED_SLEEP_FILE, 'w') as f:
        json.dump(list(ids), f)

def workout_to_event(workout):
    # Handle Zulu time (Z) in Whoop timestamps
    start = datetime.fromisoformat(workout['start'].replace('Z', '+00:00')).isoformat()
    end = datetime.fromisoformat(workout['end'].replace('Z', '+00:00')).isoformat()
    
    # Get workout type/sport
    sport_id = workout.get('sport_id', -1)
    sport_name = get_sport_name(sport_id)
    
    # Calculate duration in minutes
    start_time = datetime.fromisoformat(workout['start'].replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(workout['end'].replace('Z', '+00:00'))
    duration_minutes = int((end_time - start_time).total_seconds() / 60)
    
    # Get metrics from score
    score = workout.get('score', {})
    strain = score.get('strain', 0)
    calories = score.get('kilojoule', 0) * 0.239  # Convert kJ to calories
    max_heart_rate = score.get('max_heart_rate', 0)
    avg_heart_rate = score.get('average_heart_rate', 0)
    
    # Build description with all metrics
    description = f"""Whoop Workout Details:
• Workout ID: {workout['id']}
• Duration: {duration_minutes} minutes
• Strain: {strain:.1f}
• Calories Burned: {calories:.0f} cal
• Max Heart Rate: {max_heart_rate} bpm
• Avg Heart Rate: {avg_heart_rate} bpm
• Sport ID: {sport_id}"""
    
    return {
        'summary': sport_name,
        'description': description,
        'start': {'dateTime': start, 'timeZone': 'UTC'},
        'end': {'dateTime': end, 'timeZone': 'UTC'},
    }

def get_sport_name(sport_id):
    """Convert Whoop sport ID to readable name"""
    sport_names = {
        -1: "Activity",
        0: "Running",
        1: "Cycling",
        16: "Baseball",
        17: "Basketball",
        18: "Rowing",
        19: "Fencing",
        20: "Field Hockey",
        21: "Football",
        22: "Golf",
        24: "Ice Hockey",
        25: "Lacrosse",
        27: "Rugby",
        28: "Sailing",
        29: "Skiing",
        30: "Soccer",
        31: "Softball",
        32: "Squash",
        33: "Swimming",
        34: "Tennis",
        35: "Track & Field",
        36: "Volleyball",
        37: "Water Polo",
        38: "Wrestling",
        39: "Boxing",
        42: "Dance",
        43: "Pilates",
        44: "Yoga",
        45: "Weightlifting",
        47: "Cross Country Skiing",
        48: "Functional Fitness",
        49: "Duathlon",
        51: "Gymnastics",
        52: "Hiking/Rucking",
        53: "Horseback Riding",
        55: "Kayaking",
        56: "Martial Arts",
        57: "Mountain Biking",
        59: "Powerlifting",
        60: "Rock Climbing",
        61: "Paddleboarding",
        62: "Triathlon",
        63: "Walking",
        64: "Surfing",
        65: "Elliptical",
        66: "Stairmaster",
        70: "Meditation",
        71: "Other",
        73: "Diving",
        74: "Operations - Tactical",
        75: "Operations - Medical",
        76: "Operations - Flying",
        77: "Operations - Water",
        82: "Ultimate",
        83: "Climber",
        84: "Jumping Rope",
        85: "Australian Football",
        86: "Skateboarding",
        87: "Coaching",
        88: "Ice Bath",
        89: "Commuting",
        90: "Gaming",
        91: "Snowboarding",
        92: "Motocross",
        93: "Caddying",
        94: "Obstacle Course Racing",
        95: "Motor Racing",
        96: "HIIT",
        97: "Spin",
        98: "Jiu Jitsu",
        99: "Manual Labor",
        100: "Cricket",
        101: "Pickleball",
        102: "Inline Skating",
        103: "Box Fitness",
        104: "Spikeball",
        105: "Wheelchair Pushing",
        106: "Paddle Tennis",
        107: "Barre",
        108: "Stage Performance",
        109: "High Stress Work",
        110: "Parkour",
        111: "Gaelic Football",
        112: "Hurling/Camogie",
        113: "Circus Arts",
        121: "Massage Therapy",
        123: "Strength Trainer",
        125: "Watching Sports",
        126: "Assault Bike",
        127: "Kickboxing",
        128: "Stretching",
        230: "Table Tennis",
        231: "Badminton",
        232: "Netball",
        233: "Sauna",
        234: "Disc Golf",
        235: "Yard Work",
        236: "Air Compression",
        237: "Percussive Massage",
        238: "Paintball",
        239: "Ice Skating",
        240: "Handball",
        248: "F45 Training",
        249: "Padel",
        250: "Barry's",
        251: "Dedicated Parenting",
        252: "Stroller Walking",
        253: "Stroller Jogging",
        254: "Toddlerwearing",
        255: "Babywearing",
        258: "Barre3",
        259: "Hot Yoga",
        261: "Stadium Steps",
        262: "Polo",
        263: "Musical Performance",
        264: "Kite Boarding",
        266: "Dog Walking",
        267: "Water Skiing",
        268: "Wakeboarding",
        269: "Cooking",
        270: "Cleaning",
        272: "Public Speaking"
    }
    
    return sport_names.get(sport_id, f"Sport {sport_id}")

def sleep_to_event(sleep):
    """Convert Whoop sleep data to Google Calendar event"""
    start = datetime.fromisoformat(sleep['start'].replace('Z', '+00:00')).isoformat()
    end = datetime.fromisoformat(sleep['end'].replace('Z', '+00:00')).isoformat()
    start_time = datetime.fromisoformat(sleep['start'].replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(sleep['end'].replace('Z', '+00:00'))
    duration_hours = (end_time - start_time).total_seconds() / 3600
    duration_minutes = int((end_time - start_time).total_seconds() / 60)

    score = sleep.get('score', {})
    stage = score.get('stage_summary', {})
    light_sleep = stage.get('total_light_sleep_time_milli', 0) / 60000
    deep_sleep = stage.get('total_slow_wave_sleep_time_milli', 0) / 60000
    rem_sleep = stage.get('total_rem_sleep_time_milli', 0) / 60000
    awake = stage.get('total_awake_time_milli', 0) / 60000
    sleep_cycles = stage.get('sleep_cycle_count', 0)
    disturbances = stage.get('disturbance_count', 0)
    in_bed = stage.get('total_in_bed_time_milli', 0) / 60000
    no_data = stage.get('total_no_data_time_milli', 0) / 60000

    sleep_perf = score.get('sleep_performance_percentage', 0)
    sleep_eff = score.get('sleep_efficiency_percentage', 0)
    sleep_cons = score.get('sleep_consistency_percentage', 0)
    resp_rate = score.get('respiratory_rate', 0)

    description = f"""Whoop Sleep Details:
• Sleep ID: {sleep['id']}
• Duration: {duration_hours:.1f} hours ({duration_minutes} minutes)
• Sleep Performance: {sleep_perf:.0f}%
• Sleep Efficiency: {sleep_eff:.0f}%
• Sleep Consistency: {sleep_cons:.0f}%
• Respiratory Rate: {resp_rate:.1f} bpm
• Light Sleep: {light_sleep:.0f} min
• Deep Sleep: {deep_sleep:.0f} min
• REM Sleep: {rem_sleep:.0f} min
• Awake: {awake:.0f} min
• In Bed: {in_bed:.0f} min
• No Data: {no_data:.0f} min
• Sleep Cycles: {sleep_cycles}
• Disturbances: {disturbances}
"""
    return {
        'summary': f"Sleep ({sleep_perf:.0f}%)",
        'description': description,
        'start': {'dateTime': start, 'timeZone': 'UTC'},
        'end': {'dateTime': end, 'timeZone': 'UTC'},
    }

def sync_recent(days=7):
    """Sync workouts from the last N days"""
    whoop_token = load_whoop_token()
    whoop = WhoopAPIClientWithRefresh(whoop_token)
    gcal = GoogleCalendarClient()
    synced_ids = load_synced_ids()
    
    end_date = datetime.now().replace(tzinfo=None)
    start_date = end_date - timedelta(days=days)
    
    # Get all workouts and filter by date range
    workouts = whoop.get_workouts()
    print(f"Found {len(workouts)} total workouts")
    
    # Filter workouts by date range
    filtered_workouts = []
    for workout in workouts:
        workout_start = datetime.fromisoformat(workout['start'].replace('Z', '+00:00')).replace(tzinfo=None)
        if start_date <= workout_start <= end_date:
            filtered_workouts.append(workout)
    
    workouts = filtered_workouts
    print(f"Filtered to {len(workouts)} workouts in date range")
    
    new_ids = set()
    
    for workout in workouts:
        if workout['id'] not in synced_ids:
            event = workout_to_event(workout)
            gcal.add_event(GOOGLE_CALENDAR_ID, event)
            new_ids.add(workout['id'])
            print(f"Added workout: {workout.get('sport', 'Workout')} on {workout['start']}")
    
    save_synced_ids(synced_ids.union(new_ids))
    print(f"Synced {len(new_ids)} new workouts")

def sync_from_date(start_date_str):
    """Sync workouts from a specific date (YYYY-MM-DD format)"""
    whoop_token = load_whoop_token()
    whoop = WhoopAPIClientWithRefresh(whoop_token)
    gcal = GoogleCalendarClient()
    synced_ids = load_synced_ids()
    
    start_date = datetime.fromisoformat(start_date_str)
    end_date = datetime.now().replace(tzinfo=None)
    
    # Get all workouts and filter by date range
    workouts = whoop.get_workouts()
    print(f"Found {len(workouts)} total workouts")
    
    # Filter workouts by date range
    filtered_workouts = []
    for workout in workouts:
        workout_start = datetime.fromisoformat(workout['start'].replace('Z', '+00:00')).replace(tzinfo=None)
        if start_date <= workout_start <= end_date:
            filtered_workouts.append(workout)
    
    workouts = filtered_workouts
    print(f"Filtered to {len(workouts)} workouts in date range")
    
    new_ids = set()
    
    for workout in workouts:
        if workout['id'] not in synced_ids:
            event = workout_to_event(workout)
            gcal.add_event(GOOGLE_CALENDAR_ID, event)
            new_ids.add(workout['id'])
            print(f"Added workout: {workout.get('sport', 'Workout')} on {workout['start']}")
    
    save_synced_ids(synced_ids.union(new_ids))
    print(f"Synced {len(new_ids)} new workouts from {start_date_str}")

def delete_existing_workout_events(service, calendar_id, days=30):
    """Delete all workout events from the calendar in the last N days"""
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        start = (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start,
            timeMax=now,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        deleted_count = 0
        for event in events:
            service.events().delete(
                calendarId=calendar_id,
                eventId=event['id']
            ).execute()
            deleted_count += 1
        print(f"Deleted {deleted_count} workout events")
        return True
    except Exception as e:
        print(f"Error deleting workout events: {e}")
        return False

def delete_existing_sleep_events(service, calendar_id, days=30):
    """Delete all sleep events from the calendar in the last N days"""
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        start = (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start,
            timeMax=now,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        deleted_count = 0
        for event in events:
            service.events().delete(
                calendarId=calendar_id,
                eventId=event['id']
            ).execute()
            deleted_count += 1
        print(f"Deleted {deleted_count} sleep events")
        return True
    except Exception as e:
        print(f"Error deleting sleep events: {e}")
        return False

def refresh_whoop_token():
    with open('whoop_token.json', 'r') as f:
        token_data = json.load(f)
    refresh_token = token_data['refresh_token']
    # Prefer environment variables in CI; fall back to literals if present
    client_id = os.getenv('WHOOP_CLIENT_ID', "1173921f-1774-46c9-a6a4-78052162a7dc")
    client_secret = os.getenv('WHOOP_CLIENT_SECRET', "97e155a8a6c40212150d68dfa70b5eff3e4784b50bc19e444ec8bd349a4fadb7")
    token_url = 'https://api.prod.whoop.com/oauth/oauth2/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'offline'
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    new_token_data = response.json()
    with open('whoop_token.json', 'w') as f:
        json.dump(new_token_data, f)
    print('Whoop token refreshed!')
    return new_token_data['access_token']

# Patch WhoopAPIClient to auto-refresh on 401
class WhoopAPIClientWithRefresh(WhoopAPIClient):
    def _retry_on_401(self, method, *args, **kwargs):
        try:
            return getattr(super(), method)(*args, **kwargs)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                print('Access token expired, refreshing...')
                new_token = refresh_whoop_token()
                self.access_token = new_token
                return getattr(super(), method)(*args, **kwargs)
            raise
    def get_workouts(self, *args, **kwargs):
        return self._retry_on_401('get_workouts', *args, **kwargs)
    def get_sleeps(self, *args, **kwargs):
        return self._retry_on_401('get_sleeps', *args, **kwargs)

def main():
    parser = argparse.ArgumentParser(description='Sync Whoop workouts and sleep to Google Calendar')
    parser.add_argument('--days', type=int, default=7, help='Number of days to look back (default: 7)')
    parser.add_argument('--force', action='store_true', help='Force re-sync all workouts and sleep (delete existing and recreate)')
    parser.add_argument('--workouts-only', action='store_true', help='Sync only workouts, not sleep')
    parser.add_argument('--sleep-only', action='store_true', help='Sync only sleep, not workouts')
    args = parser.parse_args()

    whoop_token = load_whoop_token()
    whoop = WhoopAPIClientWithRefresh(whoop_token)
    gcal = GoogleCalendarClient()

    # Calculate start and end datetimes for the range
    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(days=args.days)
    start_iso = start_dt.isoformat().replace('+00:00', 'Z')
    end_iso = end_dt.isoformat().replace('+00:00', 'Z')

    # Sync workouts
    if not args.sleep_only:
        print("\n=== SYNCING WORKOUTS ===")
        if args.force:
            print("Force mode: Deleting existing workout events...")
            delete_existing_workout_events(gcal.service, GOOGLE_CALENDAR_ID, days=args.days)
            print("Existing workout events deleted. Recreating all workouts...")

        workouts = whoop.get_workouts(start=start_iso, end=end_iso)
        if workouts:
            print(f"Found {len(workouts)} total workouts")
            cutoff_date = start_dt
            recent_workouts = [w for w in workouts if datetime.fromisoformat(w['start'].replace('Z', '+00:00')) > cutoff_date]
            print(f"Filtered to {len(recent_workouts)} workouts in date range")
            synced_ids = load_synced_ids() if not args.force else set()
            new_ids = set()
            for workout in recent_workouts:
                if args.force or workout['id'] not in synced_ids:
                    event = workout_to_event(workout)
                    gcal.add_event(GOOGLE_CALENDAR_ID, event)
                    new_ids.add(workout['id'])
                    print(f"Added workout: {get_sport_name(workout.get('sport_id', -1))} on {workout['start']}")
            if not args.force:
                save_synced_ids(synced_ids.union(new_ids))
            print(f"Synced {len(new_ids)} new workouts")
        else:
            print("No workouts found.")

    # Sync sleep
    if not args.workouts_only:
        print("\n=== SYNCING SLEEP ===")
        if args.force:
            print("Force mode: Deleting existing sleep events...")
            delete_existing_sleep_events(gcal.service, SLEEP_CALENDAR_ID, days=args.days)
            print("Existing sleep events deleted. Recreating all sleep...")

        sleep_data = whoop.get_sleeps(start=start_iso, end=end_iso)
        if sleep_data:
            print(f"Found {len(sleep_data)} total sleep records")
            cutoff_date = start_dt
            recent_sleep = [s for s in sleep_data if s.get('start') and s.get('end') and datetime.fromisoformat(s['start'].replace('Z', '+00:00')) > cutoff_date]
            # Filter out sleep events longer than 16 hours
            filtered_sleep = []
            for s in recent_sleep:
                start = datetime.fromisoformat(s['start'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(s['end'].replace('Z', '+00:00'))
                duration = (end - start).total_seconds() / 3600
                if 2 < duration < 16:
                    filtered_sleep.append(s)
            print(f"Filtered to {len(filtered_sleep)} valid sleep records in date range")
            synced_sleep_ids = load_synced_sleep_ids() if not args.force else set()
            new_sleep_ids = set()
            for sleep in filtered_sleep:
                if args.force or sleep['id'] not in synced_sleep_ids:
                    event = sleep_to_event(sleep)
                    gcal.add_event(SLEEP_CALENDAR_ID, event)
                    new_sleep_ids.add(sleep['id'])
                    start = sleep['start']
                    end = sleep['end']
                    duration_hours = (datetime.fromisoformat(end.replace('Z', '+00:00')) - datetime.fromisoformat(start.replace('Z', '+00:00'))).total_seconds() / 3600
                    print(f"Added sleep: {duration_hours:.1f}h on {start}")
            if not args.force:
                save_synced_sleep_ids(synced_sleep_ids.union(new_sleep_ids))
            print(f"Synced {len(new_sleep_ids)} new sleep records")
        else:
            print("No sleep data found.")

if __name__ == '__main__':
    main() 