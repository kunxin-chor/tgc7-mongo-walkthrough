# See all databases

```
show databases
```
# Use a databases

```
use sample_airbnb
```

The variable `db` will refer to the database we are using now

# Show the collections in a databases
Collections are analgous to tables in SQL:

```
show collections
```

# Queries

```
db.listingsAndReviews.find()
```

In general, the generic structure of the command is:

```
db.<collection_name>.find()
```

Adding .pretty() allows us to format the output nicely.

```
db.listingsAndReviews.find().pretty()
```

Adding .limit(x) to limit to the first x number of records.

```
db.listingsAndReviews.find().pretty().limit(2)
```

## Find listings by critera

Find all the listings with only 2 beds.
```
db.listingsAndReviews.find({
    'beds': 2
}).pretty().limit(5)
```
## Projecting
Similiar to how we do "SELECT <columns>" in SQL, we can also say which fields in the results:


Find all the listings with 2 beds and display only the name, the address and the beds
```
db.listingsAndReviews.find({
    'beds':2
}, {
    'name':1, 'address':1, 'beds':1
}).pretty().limit(5)
```

Find all the lisings and display only the name, the number of the beds, and ONLY the country field from address
```
db.listingsAndReviews.find({
    'beds':2
}, {
    'name':1,
    'address.country':1,
    'beds':1
}).pretty().limit(5)
```

Find all the listings in the Brazil

```
db.listingsAndReviews.find({
    'address.country':'Brazil'
}, {
    'name':1,
    'address.counry':1,
    'address.suburb':1,
    'address.street':1
}).pretty().limit(5);
```

## Find by multiple critera

Add the new critera to the first argument to the `find` function. 

To find listings with 2 beds and 2 bedrooms:

```
db.listingsAndReviews.find({
    'beds': 2,
    'bedrooms':2
}, {
    'name':1,
    'beds':1,
    'bedrooms':1
}).pretty().limit(10)
```

## Find by a range or inequality

We can `$gt` or `$lt` to represent greater than or less than.

```
db.listingsAndReviews.find({
    'beds': {
        '$gt':3
    }
}, {
    'name':1,
    'beds':1
}).pretty().limit(10)
```

Find all listings with less than 3 beds:
```
db.listingsAndReviews.find({
    'beds': {
        '$lt':3
    }
}, {
    'name':1,
    'beds':1
}).pretty().limit(10)
```

`$gte`is `greater than or equal` and `$lte` is lesser than or equal.

```
db.listingsAndReviews.find({
    'beds':{
        '$gte':4,
        '$lte':8
    }
}, {
    'beds':1,
    'name':1
}).pretty().limit(10)
```

Find listings with 3 bedrooms but with 4 to 6 beds:
```
db.listingsAndReviews.find({
    'beds':{
        '$gte':4,
        '$lte':6
    },
    'bedrooms':3
}, {
    'beds':1,
    'name':1,
    'bedrooms':1
}).pretty().limit(10)
```

We can actually simplify it like this:
```
let criteria = {
    'beds':{
        '$gte':4,
        '$lte':6
    },
    'bedrooms':3
};

let projection = {
    'beds':1,
    'name':1,
    'bedrooms':1
};

db.listingsAndReviews.find(criteria, projection);
```

## Find by an element in an array
```
db.listingsAndReviews.find({
    'amenities':'Washer'
},
{
    'name':1,
    'amenities':1
}).pretty().limit(5)
```

## Find by specific elements in an array
Show all listings that have BOTH washer and dryers

```
db.listingsAndReviews.find({
    'amenities': {
        '$all':['Washer', 'Dryer']
    }
},
{
    'name':1,
    'amenities':1
}).pretty().limit(5)
```

## Find listings that include ONE of the specific elements in an array

```
db.listingsAndReviews.find({
    'amenities':{
        '$in':['TV', 'Cable TV']
    }
},{
    'name':1,
    'amenities':1
}).pretty().limit(5)
```

```
db.listingsAndReviews.find({
    'amenities':{
        '$in':['Kitchen', 'Microwave']
    }
},{
    'name':1,
    'amenities':1
}).pretty().limit(10)
```

## Find all listings that are either in Canada or Brazil
```
db.listingsAndReviews.find({
    'address.country':{
        '$in':['Brazil', 'Canada']
    }
}, {
    'name':1,
    'address.country':1
}).pretty()

```

## How select by its objectId
```
use sample_mflix;
db.movies.find({
    '_id':ObjectId('573a1390f29313caabcd4803')
}).pretty()
```

## Find all listings which have reviewd by Bart

```
db.listingsAndReviews.find({
    'reviews':{
        '$elemMatch': {
            'reviewer_name':'Bart'
        }
    }
}, {
    'name':1,
    'reviews.$':1
}).pretty().limit(5)
```

## Match by string
Something like `select * from customers where customerName like '%gift%'`

Search for all listings which has 'spacious' in its name, regardless of casing

```
db.listingsAndReviews.find({
    'name':{
        '$regex':"Spacious", '$options':'i'
    }
}, {
    'name':1
})
```

## Count how many listings there are in total
```
db.listingsAndReviews.find().count()
```

## Show all listings that >= 6 amentities

```
db.listingsAndReviews.find({
    'amenities.6': {
        "$exists":true
    }
},{
    'name':1, 'amenities':1
}).pretty()
```
## Compounds criteras: 'AND' or 'OR' or 'NOT'

Find all the listings in Brazil OR listings from Canada that has more than 5 bedrooms
```
db.listingsAndReviews.find({
    '$or':[
        {
            'address.country':'Brazil'
        },
        {
            'address.country':'Canada',
            'bedrooms': {
                '$gte':5
            }
        }
    ]
}, {
    'name':1,
    'bedrooms':1,
    'address.country':1
}).pretty()
```

### Find all listings NOT from Brazil or Canada
```
db.listingsAndReviews.find({
   'address.country': {
       '$not': {
           $in:['Brazil', 'Canada']
       }
   }
}, {
    'name':1,
    'address.country':1
}).pretty()
```

# Create a database
1. Use the new database
```
use animal_shelter
```

## General syntax for inserting into a collection

The `animals` collection does not have to exist for us to insert into it.

```
db.animals.insert({
    'name':'Fluffy',
    'age': 3,
    'breed':'Golden Retriever',
    'type':'Dog'
})
```

## Insert many
```
db.animals.insertMany([
    {
        'name':'Dazzy',
        'age': 35,
        'breed':'Greyhound',
        'type':'Dog'
    },
    {
        'name':'Timmy',
        'age': 1,
        'breed':'Border Collie',
        'type':'Dog'
    }
])
```

## To Update by replacing the existing key with a new document
```
db.animals.update({
    '_id':ObjectId("5f33aa91bf91d0dd5c1440de")
}, {
    "name" : "Timmy",
    "age" : 1.5,
    "breed" : "German Shepherd",
    "type" : "Dog"
})
```

## To update by specifying new values for specific fields:

```
db.animals.update({
        '_id':ObjectId("5f33aa91bf91d0dd5c1440de")
}, {
    '$set': {
        'name':'Thunder'
    }
})
```

## Delete
```
db.animals.remove({
    '_id': ObjectId("5f33aa91bf91d0dd5c1440dd")
})
```

## Managing collections 

Let's say each dog has a checkup array.

```
db.animals.insert({
    'name':'Cookie',
    'age': 3,
    'breed':'Lab Retriever',
    'type':'Dog',
    'checkups':[]
})

db.animals.insert({
    'name':'Frenzy',
    'age': 1,
    'breed':'Wild Cat',
    'type':'Cat',
    'checkups':[
        {
            'id':ObjectId(),
            'name': 'Dr Chua',
            'diagnosis':'Heartworms',
            'treatment':'Steriods'

        }
    ]
})
```

### Add a new sub-document (i.e a new object) to an array
Suppose Cookie visited a vet for the first time and we store the checkup information.

(Adding a new element to an array)
```
db.animals.update({
    '_id':ObjectId("5f33acfbbf91d0dd5c1440df"),
}, {
    '$push': {
        'checkups': {
            '_id':ObjectId(),
            'name':'Dr Tan',
            'diagnosis':'Diabetes',
            'treatment':'Medication'
        }
    }
})
```

### Remove a sub-document from an array

Pull a checkup element by its id

```
db.animals.update({
    '_id':ObjectId("5f33acfbbf91d0dd5c1440df")
}, {
    '$pull': {
        'checkups': {
              '_id':ObjectId("5f33addebf91d0dd5c1440e2")
        }
    }
})
```

### Update an existing element in an array of a document

We use `$elemMatch` in the critera to find the exact element in the array. And be sure 
to use `$` to refer to the matched element later when we do the change.

```
db.animals.update({
    'checkups': {
        '$elemMatch': {
            '_id': ObjectId("5f33b0e3bf91d0dd5c1440e4")
        }
    }
}, {
    '$set': {
        'checkups.$.name':'Dr Su'
    }
})
```

Alternatively?

```
db.animals.update({
    'checkups._id': ObjectId("5f33b0e3bf91d0dd5c1440e4")
}, {
    '$set': {
        'checkups.$.name':'Dr Zhao',
        'checkups.$.date': ISODate()
    }
})
```


## Unset a field
```
db.animals.update({
    '_id':ObjectId("5f33acfbbf91d0dd5c1440df")
}, {
    '$unset': {
        'date':""
    }
})
```

# Using Mongo with Python

## The dependencies

```
pip3 install dnspython
pip3 install pymongo
```

## Find the connection string
Click on the `Connect` button of your cluster and select `Connect to an application`.

Select driver to be `Python` and version to be `3.11 or later`

## Define the connection string and database name

```
MONGO_URI = '<connection string>'
DB_NAME = 'sample_airbnb'
```

Rememebr to replace the `<password>` in the connection string with your actual password.

# Use environmental variables to hide the MONGO_URI

1. Install `python-dotenv` dependency

2. Create `.env` file in the same folder as `app.py`

# Generic Pesudo-code for CRUD 

## READ

1. Get all the data from the database (regardless whether it's just a JSON file, or SQL, or Mongo)

2. Pass the data into the template

