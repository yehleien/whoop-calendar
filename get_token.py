#!/usr/bin/env python3
"""
Simple script to get Whoop access token via OAuth
"""

from whoop_oauth import start_oauth_server
import json
import os

def save_token(token_data):
    """Save token data to a file"""
    with open('whoop_token.json', 'w') as f:
        json.dump(token_data, f, indent=2)
    print("Token saved to whoop_token.json")

def main():
    print("Starting Whoop OAuth flow...")
    print("This will open your browser for authorization.")
    print("After authorizing, you'll be redirected to localhost:5001")
    print("The access token will be saved to whoop_token.json")
    print()
    
    oauth = start_oauth_server()
    
    print("Waiting for authorization...")
    input("Press Enter after completing the authorization in your browser...")
    
    if oauth.access_token:
        token_data = {
            'access_token': oauth.access_token,
            'refresh_token': getattr(oauth, 'refresh_token', None),
            'client_id': oauth.client_id,
            'client_secret': oauth.client_secret
        }
        save_token(token_data)
        print(f"Access token: {oauth.access_token}")
        if token_data.get('refresh_token'):
            print(f"Refresh token: {token_data['refresh_token']}")
        print("Token saved successfully!")
    else:
        print("No access token received. Please try again.")
        print("Make sure you completed the authorization in your browser.")

if __name__ == '__main__':
    main() 