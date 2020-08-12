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
        '$in':['Kitchen', 'Mircowave']
    }
},{
    'name':1,
    'amenities':1
}).pretty().limit(5)
```