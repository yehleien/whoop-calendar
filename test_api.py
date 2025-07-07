#!/usr/bin/env python3
"""
Test Whoop API connection and endpoints
"""

from whoop_api import WhoopAPIClient
from sync import load_whoop_token

def main():
    print("Testing Whoop API connection...")
    
    # Load token
    whoop_token = load_whoop_token()
    whoop = WhoopAPIClient(whoop_token)
    
    # Test basic connection
    print("\n1. Testing user profile...")
    try:
        profile = whoop.test_connection()
        print("✅ User profile works!")
        print(f"User: {profile}")
    except Exception as e:
        print(f"❌ User profile failed: {e}")
    
    # Test workout endpoint
    print("\n2. Testing workout endpoint...")
    try:
        workouts = whoop.get_workouts()
        print("✅ Workout endpoint works!")
        print(f"Found {len(workouts)} workouts")
    except Exception as e:
        print(f"❌ Workout endpoint failed: {e}")
    
    # Test cycles endpoint
    print("\n3. Testing cycles endpoint...")
    try:
        cycles = whoop.get_cycles()
        print("✅ Cycles endpoint works!")
        print(f"Found {len(cycles)} cycles")
    except Exception as e:
        print(f"❌ Cycles endpoint failed: {e}")
    
    # Test activities endpoint
    print("\n4. Testing activities endpoint...")
    try:
        activities = whoop.get_activities()
        print("✅ Activities endpoint works!")
        print(f"Found {len(activities)} activities")
    except Exception as e:
        print(f"❌ Activities endpoint failed: {e}")

if __name__ == '__main__':
    main() 