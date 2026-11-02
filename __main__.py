import requests
import json
from datetime import datetime, date, timedelta
from collections import defaultdict
from flask import Flask, render_template
from src.weather_predict import WeatherPredictor

#Construct a WeatherPredictor object (defined in weather_predict.py)
#and train it using the provided csv file
#which was downloaded from the NOAA website
wp=WeatherPredictor('data/2025_weather_data.csv')
wp.clean_data()
wp.train()
print('Model training complete! Starting Application...')

#set app to use the current file name
app = Flask(__name__)

#Lat and Lon will be used as the location for the weather queries
#I have hardcoded them to the location of Clark College
LAT, LON = 45.63, -122.65

#NOAA API requires a token which is free to request, but has limited access that
#exceeds the requirements of this application, so we should not run into any problems
#The request form is on their website, that is how I retrieved my token

#these will be used to query only the last ten days from NOAA, as well as parse the NWS forecast JSON
#for today's temperatures
end_date=date.today()
start_date=end_date-timedelta(days=9)

NOAA_HEADER = {"token": "mVpLMAcjttMghaYaCpbJYkOjXEeXucPc"}
NOAA_URL = 'https://www.ncei.noaa.gov/cdo-web/api/v2/data'
NOAA_PARAMS = {
    "datasetid": "GHCND",
    "stationid": "GHCND:USW00094298",
    "startdate": start_date.isoformat(),
    "enddate": end_date.isoformat(),
    "datatypeid": ["TMAX", "TMIN"],
    "units": "standard",
    "limit": 1000,
}

#query the NOAA api to get the last 10 days of forecast data
#which is unavailable through the NWS api
old_weather=requests.get(
    NOAA_URL, params=NOAA_PARAMS, headers=NOAA_HEADER, timeout=10
)
old_weather.raise_for_status()
#filter out everything but the data we want to parse
old_weather=old_weather.json().get("results", [])

#parse the returned forecast data from NOAA and convert it into 
#a list of JSON objects each containing fields defined below,
#under old_weather
by_day=defaultdict(dict)
for record in old_weather:
    day=record["date"][:10]
    by_day[day][record["datatype"]]=record["value"]

old_weather=[
    {
        "date": day,
        "high": str(values["TMAX"]) if "TMAX" in values else None,
        "low": str(values["TMIN"]) if "TMIN" in values else None,
        "conditions": None,
        "precip": None,
        "wind": None,
    }
    for day, values in sorted(by_day.items())
]

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
forecast=forecast.json()

#application home page logic
@app.route("/")
def home():
    #use the data returned from NWS api to render a basic weather data home page
    try:
        return render_template("index.html", point=point, forecast=forecast)

    #display error info to user if error
    except (requests.RequestException, KeyError, ValueError) as e:
        return render_template("index.html", error=str(e))

#application 'weather predictor' page logic
@app.route("/predict")
def predict():
    #extract today's low temperature from the forecast json
    periods=forecast["properties"]["periods"]
    matching_period=next(
        (
            period for period in periods
            if period["startTime"][:10] == end_date.isoformat()
                and period["isDaytime"] is False
        ),
        None,
    )
    #if we found today's date inside the NWS forecast json (should always be the case)
    if matching_period:
        temperature=int(matching_period["temperature"])
    #On error, alert the user
    else:
        return render_template("predictor.html", error='Error extracting min temp for model prediction!')

    #convert end_date (today's date) into a number representing the day of the year 1-365
    date_int=datetime.strptime(end_date.isoformat(), "%Y-%m-%d").timetuple().tm_yday

    #increment date_int by one to have it represent tomorrow
    #should ideally test for last day of the year edge cases for leap and non leap year here
    #ex. if incrementing date_int goes to 366 we would need to check if leap year or not before deciding whether to
    #reset back to 1
    date_int+=1

    #have our WeatherPredictor predict tomorrow's high temp based on today's low and tomorrow's date_int
    prediction=wp.predict(date_int, temperature)
    my_forecast={ 
        "title": "Linear Regression Model -- 2025 data Pearson Airport",
        "high": round(prediction[0], 1), #round the prediction to one decimal place
        "unit": "F",
        "notes": "This result was generated based on today's low temp, as well as tomorrow's date"
    }

    #render the weather prediction page with all of the 
    #corresponding data
    try:
        return render_template(
            "predictor.html", 
            history=old_weather, 
            forecast=forecast,
            my_forecast=my_forecast)
    #display the home screen with an error if something failed
    except:
        return render_template(
            "index.html", 
            error=str(e))

if __name__ == "__main__":
    app.run()
