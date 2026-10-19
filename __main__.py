from flask import Flask, render_template
import requests as req

#name the app object with current file name
app=Flask(__name__)

#url to wttr.in weather info for portland
WTTR_URL="https://wttr.in/Portland?format=j1"

@app.route("/")
def home():
    #attempt to get the info from wttr.in, waiting 10 seconds
    try:
        response=req.get(WTTR_URL, timeout=10)
        response.raise_for_status()
        #successful response case
        return render_template("index.html", weather=response.json())

    except (requests.RequestException, ValueError) as e:
        #invalid response case
        return render_template("index.html", error=str(e))

#run if we are the correct file, run the app!
if __name__ == "__main__":
    app.run(debug=True)
