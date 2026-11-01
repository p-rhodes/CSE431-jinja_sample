from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
import pandas as pd

class WeatherPredictor:
    def __init__(self, file_name: str):
        self.model=LinearRegression()
        self.df=pd.read_csv(file_name)

    def clean_data(self):
        #drop any empty temperature results
        self.df=self.df.dropna(subset=["TMIN"])
        self.df=self.df.dropna(subset=["TMAX"])

        #convert date fields from str to ytd integer (Ex. Jan 1=1, Dec 31=365)
        self.df["DATE"]=pd.to_datetime(self.df["DATE"], errors="coerce")
        self.df["DATE"]=self.df["DATE"].dt.dayofyear.astype("int")

    def train(self):
        inputs=self.df[["DATE", "TMIN"]]
        outputs=self.df["TMAX"]

        i_train, i_test, o_train, o_test=train_test_split(
            inputs, outputs, test_size=0.35, random_state=42
        )

        self.model.fit(i_train, o_train)

        test_outputs=self.model.predict(i_test)
        print(f'''
            Training Results:\n
            r2: {r2_score(o_test, test_outputs)}\n
            MSE: {mean_squared_error(o_test, test_outputs)}\n''')

    def predict(self, date: int, tmin: int):
        data=pd.DataFrame({
            "DATE": [date],
            "TMIN": [tmin]
        })
        return self.model.predict(data)

    def to_string(self) -> str:
        return f'''
            Head:\n{self.df.head()}\n
            Shape:\n{self.df.shape}\n
            Info:\n{self.df.info()}\n'''
