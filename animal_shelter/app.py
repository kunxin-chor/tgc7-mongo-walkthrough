from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pymongo
from dotenv import load_dotenv
from bson.objectid import ObjectId
import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

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
    animal_types = db.animal_types.find()
    return render_template('create_animal.template.html', errors={},
                           animal_types=animal_types)


@app.route('/animals/create', methods=["POST"])
def process_create_animal():

    # retrieve the information from the form
    name = request.form.get('name')
    breed = request.form.get('breed')
    age = request.form.get('age')
    animal_type_id = request.form.get('type')

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

    # if there are any errors, go back to the form and
    # tell the user to try again
    if len(errors) > 0:
        animal_types = db.animal_types.find()
        flash("Unable to create animal", "danger")
        return render_template('create_animal.template.html', errors=errors,
                               previous_values=request.form,
                               animal_types=animal_types)

    # fetch the information about the animal type by its id
    animal_type = db.animal_types.find_one({
        '_id': ObjectId(animal_type_id)
    })

    # if there are no errors, insert the new animal

    # create the query
    new_record = {
        'name': name,
        'breed': breed,
        'age': age,
        'type': {
            '_id': ObjectId(animal_type_id),
            'name': animal_type["name"]
        }
    }

    # execute the query
    db.animals.insert_one(new_record)

    flash("New animal has been added", "success")

    return redirect(url_for('show_animals'))


@app.route('/animals/update/<animal_id>')
def show_update_animal(animal_id):
    animal = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })
    animal_types = db.animal_types.find()
    return render_template('update_animal.template.html', animal=animal,
                           animal_types=animal_types)


@app.route('/animals/update/<animal_id>', methods=["POST"])
def process_update_animal(animal_id):

    # extract out the form fields
    name = request.form.get('name')
    breed = request.form.get('breed')
    age = request.form.get('age')
    animal_type_id = request.form.get('type')

    # check if valid

    # modify the record

    animal_type = db.animal_types.find_one({
        '_id': ObjectId(animal_type_id)
    })

    db.animals.update_one({
        '_id': ObjectId(animal_id)
    }, {
        '$set': {
            'name': name,
            'breed': breed,
            'age': age,
            'type':  {
                '_id': ObjectId(animal_type_id),
                'name': animal_type["name"]
            }
        }
    })

    return redirect(url_for('show_animals'))


@ app.route('/animals/delete/<animal_id>')
def show_delete_animal(animal_id):
    animal = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })
    return render_template('show_delete_animal.template.html', animal=animal)


@ app.route('/animals/delete/<animal_id>', methods=["POST"])
def process_delete_animal(animal_id):
    db.animals.remove({
        '_id': ObjectId(animal_id)
    })

    return redirect(url_for('show_animals'))


@app.route('/animals/<animal_id>/checkups')
def view_animal_checkups(animal_id):
    animal = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })
    return render_template('show_animal_checkups.template.html', animal=animal)


@app.route('/animals/<animal_id>/checkup/create')
def show_create_checkup(animal_id):
    animal = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })
    vets = db.vets.find()
    return render_template('show_add_checkup.template.html', animal=animal,
                           vets=vets)


@app.route('/animals/<animal_id>/checkup/create', methods=["POST"])
def process_create_checkup(animal_id):

    # extract out the form fields
    diagnosis = request.form.get('diagnosis')
    treatment = request.form.get('treatment')
    date = request.form.get('date')
    vet_id = request.form.get('vet_id')

    # validate the fields

    # get the details of the vet because I need the vet's name
    vet = db.vets.find_one({
        '_id': ObjectId(vet_id)
    })

    # insert the new record
    db.animals.update({
        '_id': ObjectId(animal_id)
    }, {
        '$push': {
            'checkups': {
                '_id': ObjectId(),
                'vet_name': vet["name"],
                'vet_id': ObjectId(vet_id),
                'treatment': treatment,
                'diagnosis': diagnosis,
                'date': datetime.datetime.strptime(date, "%Y-%m-%d")
            }
        }
    })

    return redirect(url_for('view_animal_checkups', animal_id=animal_id))


@app.route('/checkups/<checkup_id>/update')
def show_edit_checkup(checkup_id):
    animal = db.animals.find_one({
        'checkups._id': ObjectId(checkup_id)
    }, {
        'name': 1,
        'checkups.$': 1
    })
    vets = db.vets.find()
    return render_template('show_update_checkup.template.html',
                           animal=animal, vets=vets)


@app.route('/checkups/<checkup_id>/update', methods=["POST"])
def process_update_checkup(checkup_id):

    diagnosis = request.form.get('diagnosis')
    treatment = request.form.get('treatment')
    date = request.form.get('date')
    vet_id = request.form.get('vet_id')

    vet = db.vets.find_one({
        '_id': ObjectId(vet_id)
    }, {
        'name': 1
    })

    # get the animal id
    animal = db.animals.find_one({
        'checkups._id': ObjectId(checkup_id)
    }, {
        '_id': 1
    })

    db.animals.update_one({
        'checkups._id': ObjectId(checkup_id)
    }, {
        '$set': {
            'checkups.$.diagnosis': diagnosis,
            'checkups.$.treatment': treatment,
            'checkups.$.date': datetime.datetime.strptime(date, "%Y-%m-%d"),
            'checkups.$.vet_id': ObjectId(vet_id),
            'checkups.$.vet_name': vet["name"]
        }
    })

    return redirect(url_for('view_animal_checkups', animal_id=animal['_id']))


@app.route('/checkups/<checkup_id>/delete')
def show_delete_checkup(checkup_id):
    animal = db.animals.find_one({
        "checkups._id": ObjectId(checkup_id)
    }, {
        'name': 1,
        'checkups.$': 1
    })

    return render_template('show_delete_checkup.template.html',
                           animal=animal)


@app.route('/checkups/<checkup_id>/delete', methods=["POST"])
def process_delete_checkup(checkup_id):
    animal_id = request.form.get('animal_id')

    # delete the animal's checkup specified by the checkup_id
    db.animals.update_one({
        'checkups._id': ObjectId(checkup_id)
    }, {
        '$pull': {
            'checkups': {
                '_id': ObjectId(checkup_id)
            }
        }
    })

    return redirect(url_for('view_animal_checkups', animal_id=animal_id))


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
