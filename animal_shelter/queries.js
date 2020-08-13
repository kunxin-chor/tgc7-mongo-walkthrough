use animal_shelter_actual;
db.animal_types.insertMany([
    {
        'name':'Dog'        
    },
    {
        'name': 'Cat'
    },
    {
        'name': 'Bird'
    },
    {
        'name': 'Rodent'
    }
])


db.vets.insertMany([
    {
        'name':'Dr Chua',
        'address':'Sunset Drive Lane 1 Blk 313 #01-01',
        'license_number': "AX12345"
    },
    {
        'name':'Dr Tan',
        'address':'Ang Mio Kio Ave 4 Blk 221 #02-02',
        'license_number': "DX45678"
    },

])

db.animals.update({
    '_id': ObjectId('5f34ec63319879464b4759df')
}, {
    '$push': {
        'checkups': {
            '_id':ObjectId(),
            'name': 'Dr. Chua',
            'vet_id':ObjectId("5f34ee16a9ef27b26157bbab"),
            'diagnosis':'Hiccups',
            'treatment':'Medication',
            'date':ISODate('2020-06-01')
        }

    }
})