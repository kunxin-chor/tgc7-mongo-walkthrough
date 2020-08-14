from flask import Flask, render_template, request, redirect, url_for
import pymongo  # mongo
import flask_login  # handle user login
import os
from dotenv import load_dotenv  # load in .env files

app = Flask(__name__)

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')

# set up the secret key to the Flask app
app.secret_key = SECRET_KEY

# connect to the Mongo database
client = pymongo.MongoClient(MONGO_URI)
db = client["sample_app"]


@app.route('/register')
def register():
    return render_template('register.template.html')



# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
