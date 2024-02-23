from dotenv import load_dotenv
from pprint import pprint
import requests
import os
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

def get_current_weather(city):
    request_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv("WEATHER_API_KEY"),
        "units": "metric"
    }
    weather_data = requests.get(request_url, params=params)
    return weather_data.json()

def get_location(city):
    geolocator = Nominatim(user_agent="weather-app")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    weather_data = get_current_weather(city)
    latitude, longitude = get_location(city)
    return render_template('get_weather.html', api_key=os.getenv("GOOGLE_MAP_API_KEY"), latitude=latitude, longitude=longitude, weather_data=weather_data)


if __name__ == "__main__":
    print('\n***Welcome to World Weather App!***\n')
    city = input("Enter the city: ")
    weather_data = get_current_weather(city)

    print("\n")
    pprint(weather_data)