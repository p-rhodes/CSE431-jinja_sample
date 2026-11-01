#THIS SCRIPT IS DEPRECATED AND NOT ACTUALLY USED
#I used it to rough draft some of my ideas together
#I have left it here so you can see some of the iterations
#the project went through

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

#this will be used to parse the date field of the csv into a day of the year
from datetime import datetime

#open up the training data as a dataframe
weather_frame=pd.read_csv("2025_weather_data.csv")

#drop any row where desired fields are empty
weather_frame=weather_frame.dropna(subset=["TMIN"])
weather_frame=weather_frame.dropna(subset=["TMAX"])

#print some basic debug info so I know stuff is working to start
print(f'Head:\n{weather_frame.head()}')
print(f'Shape:\n{weather_frame.shape}')
print(f'Info:\n{weather_frame.info()}')

#convert all date fields into an integer representing day of the year
#ex. Jan 1 would be 1, Jan 2 would 2, etc.
weather_frame["DATE"]=pd.to_datetime(weather_frame["DATE"], errors="coerce")
weather_frame["DATE"]=weather_frame["DATE"].dt.dayofyear.astype("int")

#print the number of T values
print(f'# of TMAX values: {weather_frame["TMAX"].size}')
print(f'# of TMIN values: {weather_frame["TMIN"].size}')

#min temps will be used to train the model
#and date
input_set=weather_frame[["DATE", "TMIN"]]

#ultimately we want the model to predict daily max temperature
predict_set=weather_frame["TMAX"]

#split the data to train the model and test the model
input_train, input_test, predict_train, predict_test=train_test_split(
    input_set, predict_set, test_size=0.5, random_state=42
)

weather_predictor=LinearRegression()
weather_predictor.fit(input_train, predict_train)

test_predictions=weather_predictor.predict(input_test)

print("r2:", r2_score(predict_test, test_predictions))
print("MSE:", mean_squared_error(predict_test, test_predictions))

mock_data=pd.DataFrame({
    "DATE": [52],
    "TMIN": [33]
})

prediction=weather_predictor.predict(mock_data)

print(f'Test Prediction: {prediction}')
