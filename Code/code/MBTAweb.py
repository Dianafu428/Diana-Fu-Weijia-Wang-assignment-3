
from flask import Flask,render_template,request
#from service import *
from mbta_helper import *

app = Flask(__name__)

# Homepage
@app.route("/")
def index():
    """By inputting a particular location, the program will search for
    the nearest station. 
    If it is not a post request, render to the error page.
    If the key does not exist, report KeyError, and return to the 400 page.
    Then based on the MBTA data, the program will search for the information
    of the nearby MBTA station.
    Eventually, if there is any error, the program will just render 
    a simple error page for the users."""
    
    return render_template("search.html",)

# Search the nearest station
@app.route("/nearest",methods=["POST"])
def nearest():
    if request.method == "POST":
        place_name = request.form['place_name']
        
        if place_name =="" or place_name is None:
            return render_template("error.html")
        #place_name = "Boston Common"
        # search the information of the nearby MBTA station
        lat, lng, name, wheelchair_boarding = get_closed_stop(place_name)
        
        return render_template("mbta_station.html", lat=lat, lng=lng, name=name, wheelchair_boarding=wheelchair_boarding,
                               place_name=place_name)
    else:
        # render a simple error page
        return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)
