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
# NEW REQUIREMENTS.TXXT
# set up all the necessary keys
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_PASSWORD') # note make sure this secret key is hidden at all times
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # initialize flask sql database
db = SQLAlchemy(app) # initialize flask sql database, db


openai.api_key = bam_key
openai.api_base = "https://bsmp2023.openai.azure.com/"
openai.api_type = 'azure'
openai.api_version = "2023-03-15-preview"
OPENAI_MODEL = "gpt-35-turbo"


# all functions

# get name of city
def reverseGeocode(coordinates):
    result = rg.search(coordinates)
     
    # result is a list containing ordered dictionary.
    return result[0]['name']


# USE THE OPENAI from the BSMP

def ai_gen(city):
  response = openai.ChatCompletion.create(
    engine=OPENAI_MODEL,
    messages=[
      {
        "role": "system",
        "content": "Get the city and retrieve the population density and only the population density, meaning only respond with the number and not any text or other characters besides digits"
      },
      {
        "role": "user",
        "content": city
      },
    ])
  
  generated_text = response['choices'][0]['message']['content']
  print(generated_text)
  
  return generated_text

# database class
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
        print(coordinates)
        city = reverseGeocode(coordinates)
        #print(type(city))
        print(city)
        #generated_text= ai_gen(city)
        firstNumFound = False


        '''for i in generated_text:
            if i.isnumeric():
                number+=i
                firstNumFound = True
            if firstNumFound:
                if i == '.' or i == ' ':
                    break'''


        # NOTE: CODE IS STILL IN PRODUCTION, WILL NOT BE ACCURATE STILL NEED TO ADD IN THE OPENAI
        p_density = 6.2
        print(p_density)
        # Add to database and commit to database
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
