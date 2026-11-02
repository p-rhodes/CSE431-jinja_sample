from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
import pandas as pd

class WeatherPredictor:
    #The class weather predictor stores a scikit model and
    #a pandas dataframe. You train it by supplying a csv with the 
    #correct fields DATE, TMIN, and TMAX

    #class constructor, needs the path to the csv
    def __init__(self, file_name: str):
        self.model=LinearRegression()
        self.df=pd.read_csv(file_name)

    #clean the data before using it to train the model
    def clean_data(self):
        #drop any empty temperature results
        self.df=self.df.dropna(subset=["TMIN"])
        self.df=self.df.dropna(subset=["TMAX"])

        #convert date fields from str to ytd integer (Ex. Jan 1=1, Dec 31=365)
        self.df["DATE"]=pd.to_datetime(self.df["DATE"], errors="coerce")
        self.df["DATE"]=self.df["DATE"].dt.dayofyear.astype("int")

    #this method will train the model, and assumes the data is cleaned
    def train(self):
        #date and min temp are the model inputs
        inputs=self.df[["DATE", "TMIN"]]
        
        #and it attempts to guess the max temp for a given day
        outputs=self.df["TMAX"]

        #split the data into training/verifying sets
        #using 35% of the data to verify
        #random_state=42 ensures the same randomized
        #splitting upon each call to train_test_split()
        i_train, i_test, o_train, o_test=train_test_split(
            inputs, outputs, test_size=0.35, random_state=42
        )

        #train the model
        self.model.fit(i_train, o_train)

        #test the model
        test_outputs=self.model.predict(i_test)

        #output the results of the training to the user
        print(f'''
            Training Results:\n
            r2: {r2_score(o_test, test_outputs)}\n
            MSE: {mean_squared_error(o_test, test_outputs)}\n''')

    #likely the most commonly called method; provide a int 1-365 representing day of the year
    #and an int representing the min temp for a given date, and the model will guess the max temp for that date
    def predict(self, date: int, tmin: int):
        data=pd.DataFrame({
            "DATE": [date],
            "TMIN": [tmin]
        })
        return self.model.predict(data)

    #provide info about the stored dataframe when called as a string
    def to_string(self) -> str:
        return f'''
            Head:\n{self.df.head()}\n
            Shape:\n{self.df.shape}\n
            Info:\n{self.df.info()}\n'''
