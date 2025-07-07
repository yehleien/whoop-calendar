#!/bin/bash

# Navigate to the script directory
cd "/Users/nick/whoop calendar/whoop calendar"

# Activate virtual environment
source ../venv/bin/activate

# Run sync and capture output
echo "Starting Whoop sync..."
output=$(python sync.py --days 7 2>&1)
exit_code=$?

# Send notification based on result
if [ $exit_code -eq 0 ]; then
    # Extract summary from output
    workout_count=$(echo "$output" | grep "Synced.*workouts" | tail -1 | grep -o '[0-9]*' | head -1)
    sleep_count=$(echo "$output" | grep "Synced.*sleep" | tail -1 | grep -o '[0-9]*' | head -1)
    
    if [ -z "$workout_count" ]; then workout_count=0; fi
    if [ -z "$sleep_count" ]; then sleep_count=0; fi
    
    osascript -e "display notification \"Synced $workout_count workouts and $sleep_count sleep records\" with title \"Whoop Sync Complete\""
else
    osascript -e "display notification \"Whoop sync failed. Check logs for details.\" with title \"Whoop Sync Error\""
fi

echo "Whoop sync completed at $(date)"
echo "$output" 