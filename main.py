from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_PASSWORD') # note make sure this secret key is hidden at all times
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # initialize flask sql database
db = SQLAlchemy(app) # initialize flask sql database, db

class locationz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String, nullable=False) # get the values z
    longitude = db.Column(db.String, nullable=False) # get the valuez
 

# start
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    db.create_all() # create database
    app.run(debug=True)
