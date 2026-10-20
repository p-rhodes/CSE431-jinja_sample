import requests
from flask import Flask, render_template

#set app to use the current file name
app = Flask(__name__)

#Lat and Lon will be used as the location for the queries
#I have hardcoded them to the location of Clark College (TBD)
LAT, LON = 45.63, -122.65

#NWS requires a header to be sent that signifies the request in some way
HEADERS = {"User-Agent": "CSE431-Weather-App-Clark-College (p.rhodes@students.clark.edu)"}

@app.route("/")
def home():
    try:
        point = requests.get(
            f"https://api.weather.gov/points/{LAT},{LON}",
            headers=HEADERS, timeout=10,
        )

        print('printing point:')
        print(type(point))
        print(point)

        point.raise_for_status()
        point = point.json()

        forecast = requests.get(
            point["properties"]["forecast"], headers=HEADERS, timeout=10
        )

        print('printing forecast:')
        print(type(forecast))
        print(forecast)

        forecast.raise_for_status()
        return render_template("index.html", point=point, forecast=forecast.json())

    except (requests.RequestException, KeyError, ValueError) as e:
        return render_template("index.html", error=str(e))

@app.route("/predict")
def predict():
    return render_template("predictor.html")

if __name__ == "__main__":
    app.run()
