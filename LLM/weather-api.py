import requests

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"  # OpenWeatherMap example

    def get_forecast(self, destination, start_date, end_date):
        """
        Retrieve weather forecast for the destination
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'q': destination,
            'start_date': start_date,
            'end_date': end_date,
            'units': 'metric'  # Temperature in Celsius
        }
        
        try:
            response = requests.get(f"{self.base_url}/forecast", 
                                    headers=headers, 
                                    params=params)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Weather API Error: {e}")
            return {}
