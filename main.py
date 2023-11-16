from flask import Flask, render_template, url_for, request, jsonify, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from passwords import *
from flask_caching import Cache
import json
import pandas as pd
import os
# NEW REQUIREMENTS.TXXT
# set up all the necessary keys
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Use in-memory caching for simplicity
app.config['SECRET_KEY'] = os.environ.get('FLASK_PASSWORD') # note make sure this secret key is hidden at all times
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # initialize flask sql database
db = SQLAlchemy(app) # initialize flask sql database, db


nycInfo = pd.read_csv('nyc_zipcodes.csv')
# all functions

# database class
class locationz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False) # get the values z
    longitude = db.Column(db.Float, nullable=False) # get the valuez
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    zipcode = db.Column(db.Integer, nullable=False) # get the integer
    city = db.Column(db.String, nullable=False)
    p_density = db.Column(db.Float, nullable=False)
   

# start
@app.route('/')
def home():
    return render_template('home.html', api_key=api_key)



# SEND THE DATA TO THE JAVASCRIPT FILE 
@app.route('/data')
def data():
    x = locationz.query.filter().all()
    all_coords = []
    for i in x:
        all_coords.append([i.latitude, i.longitude, i.date, i.p_density]) # append the latitude and longitude values, this creates a two dimensional array
    my_list = all_coords
    return jsonify(my_list)


# add data into the database
@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        req = request.get_json() # get json data which turns into string

        # NOTE ALL 3 ARE STRING VALUES 
        latitude = req['latitude']
        longitude = req['longitude']
        zipcode = req['zipcode']
        #city = req['city']
        # Print the extracted values.
        print(f'Latitude: {latitude}, Longitude: {longitude}, Zipcode: {zipcode}') # returns latitude, longitude and ZIPCODE!

        # Get the city based on the zipcode (NOTE THIS ONLY FOR NYC SO NYC ZIP CODES only - Future plans may include more cities)
        # Source of csv file: https://www.fourfront.us/data/datasets/us-population-density/ - check density.py file for more notes 
        # Brooklyn Zipcodes: 11201 - 11256
        # Queens Zipcodes: 11004 - 11697
        # New York (Manhattan) Zipcodes: 10001 - 10286
        # Bronx Zipcodes: 10451 - 10475
        # Staten Island ZipCodes: 10301 - 10314

        # use if statements to assign city value based on the zipcode data (from csv )
        city = ""
        zip = int(zipcode)
        if zip >= 11201 and zip <= 11256:
            city = 'Brooklyn'
        elif zip >= 11004 and zip<= 11697:
            city = 'Queens'
        elif zip >= 10001 and zip<= 10286:
            city = 'Manhattan'
        elif zip >= 10451 and zip<= 10475:
            city = 'Bronx'
        else:
            city = 'Staten Island'

        print(city)
        
        # Find population density using the nyc_zipcodes.csv

        p_density = nycInfo.query(f"Zip=={zip}")["density"].iloc[0]
        print(p_density)
        new_push = locationz(latitude=float(latitude), longitude=float(longitude), city=city, p_density=p_density, zipcode=zip)
        db.session.add(new_push)
        db.session.commit() 
        return redirect(url_for('home'))
    res = make_response(jsonify({"messsage":"JSON"}), 200)
    return res 


# Load the CSV data and cache it when the application starts
@app.before_first_request
def load_and_cache_csv_data():
    csv_data = pd.read_csv('parkingmeter.csv')
    cache.set('csv_data', csv_data)

# Endpoint to retrieve cached CSV data
@app.route('/cached_csv_data')
def get_cached_csv_data():
    cached_data = cache.get('csv_data')
    if cached_data is not None:
        return jsonify(cached_data.to_dict(orient='records'))
    return jsonify([])



# make a function to delete the location data (Note: Authentication not implemented yet!)
@app.route("/delete_data", methods=["POST"])
def delete_data():
    if request.method == "POST":
        # get the data from JavaScript 
        req = request.get_json()
        #print(req)

        new_req = json.loads(req)
        #new_listt = req.split()
        #print(new_listt)
        latitude = new_req['lat']
        longitude = new_req['lng']

        lat = float(latitude)
        long = float(longitude)

        print(lat, long)
        # Check if the latitude and longitude exist
        latt = locationz.query.filter_by(latitude=lat).first()
        longg = locationz.query.filter_by(longitude=long).first()
        if latt and longg:
            print("Latitude and Longitude exists")
            db.session.delete(latt)
            db.session.commit()
        else:
            print("Non exist")

    res = make_response(jsonify({"messsage":"JSON"}), 200)
    return res


if __name__ == "__main__":
    db.create_all() # create database
    #app.run(host=ip, port=5000) #NOTE USE THIS TO TEST ON A MOBILE DEVICE 
    app.run(debug=True)
