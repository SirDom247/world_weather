from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

def get_current_weather(city="Omoku Town, Nigeria"):
    request_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY"),
        "units": "metric"
    }
    response = requests.get(request_url, params=params)
    return response.json()

if __name__ == "__main__":
    print('\n***Welcome to World Weather App!***\n')
    city = input("Enter the city: ")
    weather_data = get_current_weather(city)

    print("\n")
    pprint(weather_data)