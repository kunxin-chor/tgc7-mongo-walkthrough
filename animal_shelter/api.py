from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
import datetime
from bson.json_util import dumps
import json
import animals

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = "animal_shelter_actual"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/api/animals')
def get_all_animals():
    animals = db.animals.find()
    return {
        'animals': json.loads(dumps(animals))
    }


@app.route('/api/animals', methods=["POST"])
def create_animal():

    # extract out all the fields from the request
    name = request.json.get('name')
    breed = request.json.get('breed')
    animal_type_id = request.json.get('type')
    age = request.json.get('age')

    # create the new record
    animal_type = db.animal_types.find_one({
        '_id': ObjectId(animal_type_id)
    })

    animals.create_animal(db.animals, name, breed, age, animal_type)

    # return the newly created ObjectId of the animal
    return {
        'inserted_id': str(results.inserted_id)
    }


@app.route('/api/animals/<animal_id>', methods=["PUT"])
def update_animal(animal_id):
    # extract out the form fields
    name = request.json.get('name')
    breed = request.json.get('breed')
    age = request.json.get('age')
    animal_type_id = request.json.get('type')

    # check if valid

    # modify the record 

    animal_type = db.animal_types.find_one({
        '_id': ObjectId(animal_type_id)
    })

    # db.animals.update_one({
    #     '_id': ObjectId(animal_id)
    # }, {
    #     '$set': {
    #         'name': name,
    #         'breed': breed,           
    #         'age': age,
    #         'type':  {
    #             '_id': ObjectId(animal_type_id),
    #             'name': animal_type["name"]
    #         }
    #     }
    # })

    animals.update_animal(db.animals, animal_id, name, breed,
                          age, animal_type)

    return {
        "status": "OK"
    }


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
