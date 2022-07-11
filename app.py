from flask import Flask, render_template
#import SQLAlchemy here
from flask_sqlalchemy import SQLAlchemy 

from os import environ

app = Flask(__name__)
#set the SQLALCHEMY_DATABASE_URI key
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI') or 'sqlite:///gnlDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sutura-ma-ngirr-yalla'

#create an SQLAlchemy object named `db` and bind it to your app
db = SQLAlchemy(app)

#a simple initial greeting
@app.route('/')
@app.route('/index')
def greeting():
    return render_template('greeting.html')

# app name 
@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

#uncomment the code below here when done creating database instance db and models
import routes