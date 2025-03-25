import os
import json
import requests
from dotenv import load_dotenv
from flight_api import FlightAPI
from hotel_api import HotelAPI
from weather_api import WeatherAPI
from itinerary_generator import ItineraryGenerator

class TravelPlannerApp:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # API Keys
        self.flight_api_key = os.getenv('FLIGHT_API_KEY')
        self.hotel_api_key = os.getenv('HOTEL_API_KEY')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.llm_api_key = None

    def set_llm_api_key(self, api_key):
        """
        Set the LLM API key securely
        """
        self.llm_api_key = api_key

    def validate_input(self, travel_input):
        """
        Validate the input JSON structure
        """
        required_keys = [
            'destination', 'start_date', 'end_date', 
            'num_travellers', 'travel_style', 
            'accomodation_preference', 'interests'
        ]
        
        for key in required_keys:
            if key not in travel_input:
                raise ValueError(f"Missing required key: {key}")
        
        return True

    def generate_travel_plan(self, travel_input):
        """
        Main method to generate comprehensive travel plan
        """
        # Validate input
        self.validate_input(travel_input)
        
        # Initialize API Clients
        flight_client = FlightAPI(self.flight_api_key)
        hotel_client = HotelAPI(self.hotel_api_key)
        weather_client = WeatherAPI(self.weather_api_key)
        
        # Fetch Flight Options
        flights = flight_client.search_flights(
            destination=travel_input['destination'],
            start_date=travel_input['start_date'],
            end_date=travel_input['end_date'],
            num_travelers=travel_input['num_travellers']
        )
        
        # Fetch Hotel Options
        hotels = hotel_client.search_hotels(
            destination=travel_input['destination'],
            start_date=travel_input['start_date'],
            end_date=travel_input['end_date'],
            accommodation_preference=travel_input['accomodation_preference']
        )
        
        # Fetch Weather Information
        weather_data = weather_client.get_forecast(
            destination=travel_input['destination'],
            start_date=travel_input['start_date'],
            end_date=travel_input['end_date']
        )
        
        # Prepare data for LLM
        llm_input = {
            'travel_input': travel_input,
            'flights': flights,
            'hotels': hotels,
            'weather': weather_data
        }
        
        # Generate Itinerary using LLM
        if self.llm_api_key:
            itinerary_generator = ItineraryGenerator(self.llm_api_key)
            itinerary = itinerary_generator.create_itinerary(llm_input)
            return itinerary
        else:
            print("LLM API Key not set. Cannot generate detailed itinerary.")
            return {
                'flights': flights,
                'hotels': hotels,
                'weather': weather_data
            }

def main():
    # Example usage
    travel_planner = TravelPlannerApp()
    
    # Set LLM API Key (securely from environment or user input)
    travel_planner.set_llm_api_key(os.getenv('LLM_API_KEY'))
    
    # Sample travel input
    travel_input = {
        "destination": "Paris",
        "start_date": "15/07/2024",
        "end_date": "25/07/2024",
        "num_travellers": "2",
        "travel_style": "Moderate",
        "accomodation_preference": "Best view & Experience",
        "interests": {
            "choice1": "history and culture",
            "choice2": "food",
            "choice3": "adventure"
        }
    }
    
    # Generate travel plan
    travel_plan = travel_planner.generate_travel_plan(travel_input)
    
    # Save travel plan to file
    with open('travel_plan.json', 'w') as f:
        json.dump(travel_plan, f, indent=4)

if __name__ == "__main__":
    main()
