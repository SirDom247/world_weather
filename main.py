from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
from weather import get_current_weather
from waitress import serve
import os

load_dotenv()

app = Flask(__name__)

def get_geographic_coordinates(city):
    key='AIzaSyDCxksQOZeT8W5QWaIBbTneWcH-TqsuC8M'  # Retrieve the API key from the .env file
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    try:
        # Make a request to the Google Maps Geocoding API
        response = requests.get(base_url, params={'address': city, 'key': key})
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        data = response.json()

        # Check if the response is successful and contains results
        if 'results' in data and len(data['results']) > 0:
            # Extract latitude and longitude from the response
            location = data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            return (latitude, longitude)
        else:
            # Handle errors or no results found
            return None
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        return str(e)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/weather")
def get_weather():
    city = request.args.get('city')
    latitude, longitude = get_geographic_coordinates(city)
    current_weather = get_current_weather(city)
    #local_time = get_local_time(city)
    #local_date = get_local_date(city)

    return render_template(
        "get_weather.html", 
        title=current_weather["name"],
        status=current_weather["weather"][0]["description"].capitalize(),
        temp=f"{current_weather['main']['temp']:.1f}",
        feels_like=f"{current_weather['main']['feels_like']:.1f}",
        rain=f"{current_weather['rain']['1h']:.1f}" if "rain" in current_weather else "0",
        humidity=f"{current_weather['main']['humidity']}",
        wind_speed=f"{current_weather['wind']['speed']}",
        wind_direction=f"{current_weather['wind']['deg']}",
        visibility=f"{current_weather['visibility']}",
        pressure=f"{current_weather['main']['pressure']}",
        latitude=latitude,
        longitude=longitude
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
