import requests

class HotelAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hotels.com/v1"  # Replace with actual hotel API endpoint

    def search_hotels(self, destination, start_date, end_date, accommodation_preference):
        """
        Search for available hotels based on input parameters
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'preference': accommodation_preference
        }
        
        try:
            response = requests.get(f"{self.base_url}/search", 
                                    headers=headers, 
                                    params=params)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Hotel API Error: {e}")
            return []
