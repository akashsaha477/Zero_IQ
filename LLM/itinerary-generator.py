import requests

class ItineraryGenerator:
    def __init__(self, llm_api_key):
        self.llm_api_key = llm_api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"  # OpenAI API example

    def create_itinerary(self, travel_data):
        """
        Generate detailed travel itinerary using LLM
        """
        headers = {
            'Authorization': f'Bearer {self.llm_api_key}',
            'Content-Type': 'application/json'
        }
        
        prompt = self._construct_prompt(travel_data)
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a professional travel itinerary planner."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1500,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.base_url, 
                                     headers=headers, 
                                     json=payload)
            response.raise_for_status()
            
            # Extract itinerary from response
            itinerary = response.json()['choices'][0]['message']['content']
            return self._parse_itinerary(itinerary)
        
        except requests.exceptions.RequestException as e:
            print(f"LLM API Error: {e}")
            return {}

    def _construct_prompt(self, travel_data):
        """
        Construct a detailed prompt for the LLM
        """
        return f"""
        Create a comprehensive travel itinerary based on the following details:
        
        Destination: {travel_data['travel_input']['destination']}
        Travel Dates: {travel_data['travel_input']['start_date']} to {travel_data['travel_input']['end_date']}
        Number of Travelers: {travel_data['travel_input']['num_travellers']}
        Travel Style: {travel_data['travel_input']['travel_style']}
        Interests: {', '.join(travel_data['travel_input']['interests'].values())}
        
        Available Flights: {travel_data['flights']}
        Hotel Options: {travel_data['hotels']}
        Weather Forecast: {travel_data['weather']}
        
        Please provide a detailed day-by-day itinerary with:
        - Suggested daily activities
        - Recommended restaurants
        - Transportation details
        - Estimated costs
        - Time allocations
        """

    def _parse_itinerary(self, raw_itinerary):
        """
        Parse the raw LLM output into a structured format
        """
        # Basic parsing - can be enhanced with more sophisticated parsing
        return {
            'raw_itinerary': raw_itinerary,
            'structured_itinerary': self._structure_itinerary(raw_itinerary)
        }

    def _structure_itinerary(self, raw_text):
        """
        Convert raw text to a more structured JSON format
        This is a basic implementation and might need more sophisticated parsing
        """
        # Placeholder for more advanced parsing
        return {
            'day_plans': [
                {
                    'day': 1,
                    'morning_activities': [],
                    'afternoon_activities': [],
                    'evening_activities': [],
                    'meals': {},
                    'transportation': {}
                }
                # More days can be added based on trip duration
            ]
        }
