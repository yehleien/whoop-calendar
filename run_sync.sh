#!/bin/bash

# Navigate to the script directory
cd "/Users/nick/whoop calendar/whoop calendar"

# Activate virtual environment and run sync
source ../venv/bin/activate
python sync.py --days 7

# Optional: Add notification
echo "Whoop sync completed at $(date)" 