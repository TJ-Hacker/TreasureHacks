from flask import Flask, render_template, url_for, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_PASSWORD') # note make sure this secret key is hidden at all times
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # initialize flask sql database
db = SQLAlchemy(app) # initialize flask sql database, db

class locationz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False) # get the values z
    longitude = db.Column(db.Float, nullable=False) # get the valuez
 

# start
@app.route('/')
def home():
    return render_template('home.html')

#print(locationz.query.filter().all()[0])
#print(type(locationz.query.filter().all()))

x = locationz.query.filter().all()
all_coords = []
for i in x:
    all_coords.append([i.latitude, i.longitude])

print(all_coords)

@app.route('/data')
def data():
    my_list = all_coords
    return jsonify(my_list)



@app.route('/add_data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        req = request.get_json() # get json data which turns into string
        #print(req)
        #print(type(req)) , somehow a string 
        new_listt = req.split()
        #print(new_listt)
        latitude = new_listt[2][:-1]
        longitude = new_listt[4]
        #print(latitude)
        #print(longitude)
        lat = float(latitude)
        long = float(longitude) # conver to float

        # PUSH TO DATABASE

        new_push = locationz(latitude=lat, longitude=long)
        db.session.add(new_push)
        db.session.commit()

        print(latitude, longitude)
    res = make_response(jsonify({"messsage":"JSON"}), 200)
    return res 


if __name__ == "__main__":
    db.create_all() # create database
    app.run(debug=True)
