#!/usr/bin/env python3
"""
Mock Whoop API client for testing Google Calendar integration
"""

import json
from datetime import datetime, timedelta
import random

class MockWhoopAPIClient:
    def __init__(self, access_token):
        self.access_token = access_token
    
    def get_workouts(self, start=None, end=None):
        """Return mock workout data"""
        print("Using mock Whoop API - returning sample workout data")
        
        # Generate some sample workouts
        workouts = []
        base_time = datetime.now() - timedelta(days=7)
        
        workout_types = ["Running", "Cycling", "Swimming", "Weight Training", "Yoga", "HIIT"]
        
        for i in range(5):
            workout_time = base_time + timedelta(days=i, hours=random.randint(8, 18))
            duration = random.randint(30, 120)  # 30-120 minutes
            
            workout = {
                "id": f"workout_{i+1}",
                "start": workout_time.isoformat(),
                "end": (workout_time + timedelta(minutes=duration)).isoformat(),
                "sport": random.choice(workout_types),
                "duration": duration * 60,  # in seconds
                "strain": round(random.uniform(5.0, 15.0), 1),
                "calories": random.randint(200, 800)
            }
            workouts.append(workout)
        
        return workouts

def load_whoop_token():
    """Mock token loader"""
    return "mock_token"

if __name__ == '__main__':
    # Test the mock client
    client = MockWhoopAPIClient("mock_token")
    workouts = client.get_workouts()
    print(f"Generated {len(workouts)} mock workouts:")
    for workout in workouts:
        print(f"- {workout['sport']} on {workout['start']}") 