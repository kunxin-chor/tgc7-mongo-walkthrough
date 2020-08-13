from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = "animal_shelter_actual"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/animals')
def show_animals():
    all_animals = db.animals.find()

    # we pass an empty dictionary to the template so that it won't cause error
    # alternatively, a better method is to check if the variable exists
    # in the template and set it if it doesn't. Check how we do the
    # previous_values in the route below as an example
    return render_template('show_animals.template.html', animals=all_animals)


@app.route('/animals/create')
def show_create_animal():
    return render_template('create_animal.template.html', errors={})


@app.route('/animals/create', methods=["POST"])
def process_create_animal():

    # retrieve the information from the form
    name = request.form.get('name')
    breed = request.form.get('breed')
    age = request.form.get('age')
    animal_type = request.form.get('type')

    # ACCUMULATOR
    errors = {}

    # check all the information are valid

    # check if the name is longer than 3 characters
    if len(name) < 4:
        # if the name is not valid, remember that it is wrong
        errors.update(
            name_too_short="Please ensure that name has more than 3 characters")

    # check if age is valid number
    if not age.lstrip('-').isnumeric():
        errors.update(age_is_not_a_number="Please ensure that age is a number")

    # check if age is a positive number
    elif float(age) < 1:
        errors.update(age_is_not_positive="Please ensure that age is positive")

    # check if the breed is longer than 3 characters
    if len(breed) < 4:
        # if the breed is not valid, remember that it is wrong
        errors.update(
            breed_too_short="Please ensure breed is more than 3 characters")

    # check if the type is longer than 2 characters
    if len(animal_type) < 3:
        errors.update(
            type_too_short="Please ensure that type is more than 3 characters")

    # if there are any errors, go back to the form and
    # tell the user to try again
    if len(errors) > 0:
        return render_template('create_animal.template.html', errors=errors,
                               previous_values=request.form)

    # if there are no errors, insert the new animal

    # create the query
    new_record = {
        'name': name,
        'breed': breed,
        'age': age,
        'animal_type': animal_type
    }

    # execute the query
    db.animals.insert_one(new_record)

    return redirect(url_for('show_animals'))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
