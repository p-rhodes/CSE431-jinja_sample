import requests
import json
from flask import Flask, render_template
from src.model_training.weather_predict import WeatherPredictor

wp=WeatherPredictor('src/model_training/2025_weather_data.csv')
wp.clean_data()
wp.train()
print('Model training complete! Starting Application...')

#set app to use the current file name
app = Flask(__name__)

#Lat and Lon will be used as the location for the queries
#I have hardcoded them to the location of Clark College
LAT, LON = 45.63, -122.65

#NWS requires a header to be sent that signifies the request in some way
HEADERS = {"User-Agent": "CSE431-Weather-App-Clark-College (p.rhodes@students.clark.edu)"}

#NWS uses a two request system, where the first request returns metadata for a given coordinate
point=requests.get(
    f"https://api.weather.gov/points/{LAT},{LON}",
    headers=HEADERS, timeout=10,
)
point.raise_for_status()
point=point.json()

#Inside the returned point response, there is a url
#for weather data on that coordinate
#which we use for the second request that returns the actual data we need
forecast=requests.get(
    point["properties"]["forecast"], headers=HEADERS, timeout=10
)
forecast.raise_for_status()

@app.route("/")
def home():
    try:
        return render_template("index.html", point=point, forecast=forecast.json())

    except (requests.RequestException, KeyError, ValueError) as e:
        return render_template("index.html", error=str(e))

@app.route("/predict")
def predict():
    #generate some mock historical data to use
    history=[]
    for i in range(10):
        mock_data='''{
            "date": "2024-01-01",
            "high": "56",
            "low": "32",
            "conditions": "Foggy",
            "precip": "0.12 in",
            "wind": "13 mph"
        }'''
        history.append(json.loads(mock_data))

    #generate a mock prediction to place into our forecast block
    prediction=wp.predict(237, 32)
    my_forecast=json.loads('''{
        "title": "LinearRegression Model 2025",
        "high": "64",
        "low": "32",
        "unit": "F",
        "notes": "This is mock data being used to test the Jinja HTML format"
    }''')

    try:
        return render_template(
            "predictor.html", 
            history=history, 
            forecast=forecast.json(),
            my_forecast=my_forecast)
    except:
        return render_template(
            "index.html", 
            error=str(e))

if __name__ == "__main__":
    app.run()
