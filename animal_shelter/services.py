import animals
from bson.objectid import ObjectId


def create_animal_service(data, db):
    name = data.get('name')
    breed = data.get('breed')
    animal_type_id = data.get('type')
    age = data.get('age')

    animal_type = db.animal_types.find_one({
        '_id': ObjectId(animal_type_id)
    })

    results = animals.create_animal(db.animals, name, breed, age, animal_type)

    return results
