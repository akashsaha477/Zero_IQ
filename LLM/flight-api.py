import requests

class FlightAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.flights.com/v1"  # Replace with actual flight API endpoint

    def search_flights(self, destination, start_date, end_date, num_travelers):
        """
        Search for available flights based on input parameters
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'num_travelers': num_travelers
        }
        
        try:
            response = requests.get(f"{self.base_url}/search", 
                                    headers=headers, 
                                    params=params)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Flight API Error: {e}")
            return []
