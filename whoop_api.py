import requests

class WhoopAPIClient:
    def __init__(self, access_token):
        self.base_url = 'https://api.prod.whoop.com'
        self.access_token = access_token

    def get_workouts(self, start=None, end=None):
        url = f"{self.base_url}/developer/v1/activity/workout"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        all_records = []
        next_token = None
        first = True
        while True:
            if first:
                params = {'limit': 25}
                if start:
                    params['start'] = start
                if end:
                    params['end'] = end
                first = False
            else:
                params = {'limit': 25, 'nextToken': next_token}
            print(f"Making request to: {url}")
            print(f"Headers: {headers}")
            print(f"Params: {params}")
            response = requests.get(url, headers=headers, params=params)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text[:500]}")
            response.raise_for_status()
            data = response.json()
            if 'records' in data:
                all_records.extend(data['records'])
            else:
                all_records.extend(data)
            next_token = data.get('nextToken')
            if not next_token:
                break
        return all_records
    
    def get_activities(self):
        """Get all activities (alternative endpoint)"""
        url = f"{self.base_url}/developer/v1/activity"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        print(f"Making request to: {url}")
        response = requests.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text[:500]}")
        
        response.raise_for_status()
        data = response.json()
        # The API returns data in a 'records' array
        if 'records' in data:
            return data['records']
        return data
    
    def get_cycles(self):
        """Get cycles (which contain workouts)"""
        url = f"{self.base_url}/developer/v1/cycle"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        print(f"Making request to: {url}")
        response = requests.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text[:500]}")
        
        response.raise_for_status()
        data = response.json()
        # The API returns data in a 'records' array
        if 'records' in data:
            return data['records']
        return data
    
    def test_connection(self):
        """Test basic API connection"""
        url = f"{self.base_url}/developer/v1/user/profile"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        print(f"Testing connection to: {url}")
        response = requests.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text[:500]}")
        
        data = response.json()
        # The API returns data in a 'records' array
        if 'records' in data:
            return data['records']
        return data
    
    def get_sleeps(self, start=None, end=None):
        url = f"{self.base_url}/developer/v1/activity/sleep"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        all_records = []
        next_token = None
        first = True
        while True:
            if first:
                params = {'limit': 25}
                if start:
                    params['start'] = start
                if end:
                    params['end'] = end
                first = False
            else:
                params = {'limit': 25, 'nextToken': next_token}
            print(f"Making request to: {url}")
            print(f"Headers: {headers}")
            print(f"Params: {params}")
            response = requests.get(url, headers=headers, params=params)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text[:500]}")
            response.raise_for_status()
            data = response.json()
            if 'records' in data:
                all_records.extend(data['records'])
            else:
                all_records.extend(data)
            next_token = data.get('nextToken')
            if not next_token:
                break
        return all_records 