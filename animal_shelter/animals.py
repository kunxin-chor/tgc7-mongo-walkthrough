from bson.objectid import ObjectId

def create_animal(collection, name, breed, age, animal_type):
    # create the query
    new_record = {
        'name': name,
        'breed': breed,
        'age': age,
        'type': {
            '_id': animal_type['_id'],
            'name': animal_type["name"]
        }
    }

    # execute the query
    collection.insert_one(new_record)


def update_animal(collection, animal_id, name, breed, age, animal_type):
    collection.update_one({
        '_id': ObjectId(animal_id)
    }, {
        '$set': {
            'name': name,
            'breed': breed,
            'age': age,
            'type':  {
                '_id': animal_type["_id"],
                'name': animal_type["name"]
            }
        }
    })
