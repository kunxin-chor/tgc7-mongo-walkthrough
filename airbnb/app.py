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


@app.route('/search')
def search():

    # get all the search terms
    # reminder: if the method is "GET", we retrieve the fields by accessing
    # request.args
    required_listing_name = request.args.get('listing_name')
    required_country = request.args.get('country')

    # create the query base on the search terms
    critera = {}

    if required_listing_name:
        critera['name'] = {
            '$regex': required_listing_name,
            '$options': 'i'
        }

    if required_country:
        critera['address.country'] = {
            '$regex': required_country,
            '$options': 'i'
        }

    # read in the data
    all_listings = client[DB_NAME].listingsAndReviews.find(critera)

    # pass the data to the template
    return render_template('search.template.html', listings=all_listings)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
