# Parker Rhodes | CSE431 Fundamentals of AI | Midterm Project
## Pearson Airport Weather Data Predictor

### How to Setup:
1. I recommend running within a virtual environment. I am on Linux so I used **python3 -m venv .venv** to create said environment 
   from within the project root directory
2. To activate the virtual environment, again in Linux, use **source .venv/bin/activate**
3. Now, you can install the dependencies without conflicting with existing python installations. Install them with **pip install -r requirements**
4. Once the requirements successfully install, you should be able to use **python3 \_\_main\_\_.py** to start the webapp
5. Connect to the app (localhost only for now) by connecting to **http://127.0.0.1:5000**
6. The prediction page can be accessed from **http://127.0.0.1:5000/predict**

### What it Does:
The application uses weather data from the NOAA and NWS to both display a forecast as well as use a locally trained, linear regression model 
to guess what tomorrow's max temp will be based on today's min temp. The data is stored at runtime in a Pandas dataframe and used to train a Scikit 
model in a WeatherPredictor class I wrote for the project. Upon boot, the application loads in the provided csv file and uses it to train the WeatherPredictor,
before booting up the Flask application and waiting for HTTP requests

### AI Use:
Anthropic Claude AI assistance was used to generate the HTML files within the **templates** directory. Minimal queries to **duck.ai**, often using GPT Luna, were also
occasionally used with syntax questions regarding Jinja or on the specifics of using either the NWS or NOAA APIs. All Python implementations were written by me.

### Reflections:
1. **My starting point:** Before starting this project, I already knew how to call an API and manipulate datasets in Python, but had yet to have an opportunity
   to really apply it within a given context. I thought that this project applied a lot of what we have gone over in class so far by using datasets, APIs, and 
   a basic ML model.
2. **What I learned:** I have a much greater understanding of the nuance behind API-based URLs now, and what parameters go into generating said URLs. I also had an
   opportunity to understand how what __tokens__ are, since the NOAA API requires you to submit a request for a token before you can query their API.
3. **A challenge I faced:** When I first started the project, I used the website wttr.in to get weather data, but that quickly proved unsatisfactory because
   the data it returned lacked much of the information I was looking for, and was difficult to parse. 
4. **How I responded:** Due to this, I switched to the National Weather Service API, which proved to be much more robust but unfortunately does not provide 
   historical weather data. So, I had to also query the NOAA api to get historical weather data to display on the application's prediction page.
5. **Current Limitations:** Currently, the application is hard-coded to only display weather data for Pearson Airport, and is also hard-coded to train on a csv
   file that I have provided. It also does not have links to travel between the home page and the prediction page.
6. **My Next Step:** Were I to continue the project, my next steps would be to address the current limitations by allowing the user to configure where they want 
   the application to query data from the NWS for, as well as upload their own csv to train the model. I would also add links so that the prediction page is more
   easily accessed.

### Useful Project Links:
- **https://library.noaa.gov/data/cdo**
- **https://www.weather.gov/documentation/services-web-api**
