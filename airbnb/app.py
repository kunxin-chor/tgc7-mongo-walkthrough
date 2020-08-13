from flask import Flask, render_template, request, redirect, url_for
import pymongo
import os
from dotenv import load_dotenv

# load the variables defined in the .env file into the environment
load_dotenv()

app = Flask(__name__)

# define some constants
# (constants: not to be changed while the program is running)
MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = "sample_airbnb"

# create the Mongo DB client
client = pymongo.MongoClient(MONGO_URI)


@app.route('/')
def show_listings():

    # Use the Mongo Client to access our collections
    # db.listingsAndReviews.find()
    all_listings = client[DB_NAME].listingsAndReviews.find()

    # pass the results back to the template
    return render_template('show_listings.template.html',
                           listings=all_listings)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
