from flask import Flask, render_template, url_for, request, jsonify, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from passwords import *
import json
import reverse_geocoder as rg
import pprint
import os
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_PASSWORD') # note make sure this secret key is hidden at all times
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # initialize flask sql database
db = SQLAlchemy(app) # initialize flask sql database, db

# all functions

# get name of city
def reverseGeocode(coordinates):
    result = rg.search(coordinates)
     
    # result is a list containing ordered dictionary.
    return result[0]['name']

class locationz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False) # get the values z
    longitude = db.Column(db.Float, nullable=False) # get the valuez
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    city = db.Column(db.String, nullable=False)
    p_density = db.Column(db.Float, nullable=False)
   

# start
@app.route('/')
def home():
    return render_template('home.html', api_key=api_key)

#print(locationz.query.filter().all()[0])
#print(type(locationz.query.filter().all()))



#print(all_coords)

@app.route('/data')
def data():
    x = locationz.query.filter().all()
    all_coords = []
    for i in x:
        all_coords.append([i.latitude, i.longitude, i.date]) # append the latitude and longitude values, this creates a two dimensional array
    my_list = all_coords
    return jsonify(my_list)



@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        req = request.get_json() # get json data which turns into string
        #print(req)

        new_req = json.loads(req)
        latitude = new_req['lat']
        longitude = new_req['lng']
        #print(latitude)
        #print(longitude)
        lat = float(latitude)
        long = float(longitude) # conver to float

        # PUSH TO DATABASE
        coordinates = (lat,long)
        city = reverseGeocode(coordinates)
        print(type(city))
        #print(city)
        openai.api_key = open_ai_key # USING THE OPEN AI API KEY!

        ai_response = openai.Completion.create(
    prompt=f"What is the population density of {city} and only give a number/float, no other words just one singular number",
    engine="text-davinci-002"
)
        generated_text = ai_response.choices[0].text
        print(generated_text)

        p_density = float(generated_text)
        #print(p_density)
        new_push = locationz(latitude=lat, longitude=long, city=city, p_density=p_density)
        db.session.add(new_push)
        db.session.commit()

        #print(latitude, longitude)
        return redirect(url_for('home'))
    res = make_response(jsonify({"messsage":"JSON"}), 200)
    return res 


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
    app.run(debug=True)
