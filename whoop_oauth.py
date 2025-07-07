import requests
from urllib.parse import urlencode
import webbrowser
from flask import Flask, request, redirect, url_for
import threading
import time
import secrets

class WhoopOAuth:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = "https://api.prod.whoop.com/oauth/oauth2/auth"
        self.token_url = "https://api.prod.whoop.com/oauth/oauth2/token"
        self.access_token = None

    def get_authorization_url(self):
        # Generate a random state parameter (at least 8 characters)
        self.state = secrets.token_urlsafe(16)
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'offline read:recovery read:cycles read:workout read:profile read:sleep',
            'state': self.state
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def exchange_code_for_token(self, authorization_code):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data['access_token']
        return token_data
    
    def refresh_token(self, refresh_token):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'offline'
        }
        
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data['access_token']
        return token_data

def start_oauth_server():
    app = Flask(__name__)
    oauth = WhoopOAuth(
        client_id="1173921f-1774-46c9-a6a4-78052162a7dc",
        client_secret="97e155a8a6c40212150d68dfa70b5eff3e4784b50bc19e444ec8bd349a4fadb7",
        redirect_uri="http://localhost:5001/callback"
    )
    
    @app.route('/callback')
    def callback():
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return f"Authorization error: {error} - {request.args.get('error_description', '')}"
        
        if code and state:
            # Verify state parameter matches
            if state != oauth.state:
                return "State parameter mismatch - possible CSRF attack"
            
            try:
                token_data = oauth.exchange_code_for_token(code)
                # Store refresh token in the oauth object
                oauth.refresh_token = token_data.get('refresh_token')
                print(f"Access Token: {oauth.access_token}")
                print("Refresh Token:", token_data.get('refresh_token', 'No refresh token'))
                print("Expires in:", token_data.get('expires_in', 'Unknown'), "seconds")
                print("Token data:", token_data)
                return "Authorization successful! You can close this window."
            except Exception as e:
                return f"Error: {str(e)}"
        
        return "No authorization code received or invalid state parameter"
    
    def run_server():
        app.run(host='localhost', port=5001)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser for authorization
    auth_url = oauth.get_authorization_url()
    print(f"Opening browser for authorization: {auth_url}")
    webbrowser.open(auth_url)
    
    # Wait for callback
    time.sleep(2)
    return oauth

if __name__ == '__main__':
    oauth = start_oauth_server()
    print("Waiting for authorization...")
    input("Press Enter after completing authorization...")
    print(f"Final access token: {oauth.access_token}") 