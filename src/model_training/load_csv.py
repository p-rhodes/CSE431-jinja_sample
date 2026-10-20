import pandas as pd

#open up the training data as a dataframe
weather_frame=pd.read_csv("2025_weather_data.csv")

#cast necessary columns
weather_frame=weather_frame.astype({
    #treat daily avg temp as a float
    "TAVG": "float",

    #will likely place more here eventually
})

#print some basic debug info so I know stuff is working to start
print(f'Head:\n{weather_frame.head()}')
print(f'Shape:\n{weather_frame.shape}')
print(f'Info:\n{weather_frame.info()}')

#print the number of TAVG values
print(f'# of TAVG values: {weather_frame["TAVG"].size}')
