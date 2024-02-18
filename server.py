from flask import Flask, render_template, request
from weather import get_current_weather

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return "Hello World!"

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    current_weather = get_current_weather(city)
    return render_template(
        "get_weather.html", 
        title=current_weather["name"],
        status=current_weather["weather"][0]["description"].capitalize(),
        temp=f"{current_weather['main']['temp']:.1f}",
        feels_like=f"{current_weather['main']['feels_like']:.1f}"
    )


if __name__ == "__name__":
    app.run(host="0.0.0.0", port=8000)



