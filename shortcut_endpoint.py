from flask import Flask, request, jsonify
from sync import sync_recent, sync_from_date
import sys

app = Flask(__name__)

@app.route('/sync', methods=['POST'])
def trigger_sync():
    """Default sync - last 7 days"""
    try:
        sync_recent()
        return jsonify({'status': 'success', 'message': 'Synced recent workouts'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/sync/recent/<int:days>', methods=['POST'])
def trigger_sync_recent(days):
    """Sync workouts from last N days"""
    try:
        sync_recent(days)
        return jsonify({'status': 'success', 'message': f'Synced workouts from last {days} days'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/sync/from/<date>', methods=['POST'])
def trigger_sync_from_date(date):
    """Sync workouts from a specific date (YYYY-MM-DD)"""
    try:
        sync_from_date(date)
        return jsonify({'status': 'success', 'message': f'Synced workouts from {date}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 