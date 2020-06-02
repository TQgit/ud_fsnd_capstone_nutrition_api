# Capstone Nutrition Facts API & Database

This is my capstone project for the Udacity fullstack nanodegree program. It is a Flask and SQLalchemy server utilizing a postgres database to store nutritional value data of restaurant offerings, it can be run locally and is also deployed using `gunicorn` on Heroku [Here.](https://nutrition-fsnd-capstone.herokuapp.com/) The API can be used to add, retrieve, edit and delete entries in the database utilizing Auth0 for authorization. Details on how to run the app and API usage is provided in the following documentation. 

## Getting Started

### Installing Dependencies

#### Getting Requirements Using PIP

Install dependencies by navigating to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the postgres database. The database structure is defined in models.py and utilizes db migration using flask-migrate. 

## Database Setup
With postgres running, from the project directory run the following on your terminal:
```bash
createdb nutrition
python manage.py db upgrade
```

## Running the server

To launch the Flask server from the project directory, run the following:
```bash
python app.py
```

## API

#### Base URL

This app can be run locally, the backend utilizes http://localhost:5000

#### Heroku Deployment

A live version of the app is deployed on Heroku using gunicorn here: https://nutrition-fsnd-capstone.herokuapp.com/

#### Authentication

The API uses authentication via Auth0 and utilizes a bearer token in the request header following this format:
```
{
    'Authorization': 'Bearer <JWT>'
} 
```
Registration on the live Heroku deployment will create an account with the `Contributor` role permissions and redirect to a page where your JWT token can be copied. Please use http://jwt.io to validate the token has the proper permissions attached, if no permissions are assigned, make sure to validate your email address and then relogin to get an updated token with the permissions. To test out the API with other roles, you can use the demo tokens found in the setup.sh file.

#### RBAC

The app utilizes role-based access control to assign permissions to users. The roles and attached permissions are as follows:
- Contributor (default):
    - `get:restaurants`, `get:orders`
    - `post:restaurants`, `post:orders`
- Trusted Editor:
    - All `Contributor` permissions
    - `patch:orders`
    - `delete:orders`
- Moderator:
    - All `Trusted Editor` permissions
    - `patch:restaurants`
    - `delete:restaurants`

#### Error Handling

Errors 400, 401, 403, 404, 405, 422, 500 will be returned as JSON in the following format:
```
{
    'success': False,
    'error': 404,
    'message': 'Not found'
} 
```

### Endpoints

Endpoints:
- GET '/restaurants'
- GET '/orders'
- GET '/restaurants/<int:restaurant_id>/orders'
- POST '/restaurants'
- POST '/orders'
- PATCH '/restaurants/<int:restaurant_id>'
- PATCH '/orders/<int:order_id>'
- DELETE '/restaurants/<int:restaurant_id>'
- DELETE '/orders/<int:order_id>'

The app also has a frontend homepage displaying current database data at the '/' endpoint

#### GET '/restaurants'
- Fetches the list of restaurants in the database
- Required Permission: `get:restaurants`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/restaurants
```

```
EXAMPLE RETURN

{
    "restaurants": [
        {
            "cuisine": "Fast Food",
            "id": 1,
            "name": "KFC"
        },
        {
            "cuisine": "Burgers",
            "id": 2,
            "name": "Five Guys"
        },
        {
            "cuisine": "Cafe",
            "id": 3,
            "name": "Starbucks"
        },
        {
            "cuisine": "Mexican",
            "id": 4,
            "name": "Chipotle"
        }
    ],
    "success": true
}
```

#### GET '/orders'
- Fetches the list of orders in the database
- Required Permission: `get:orders`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/orders
```

```
EXAMPLE RETURN

{
    "orders": [
        {
            "calories": 480,
            "cholesterol": 110,
            "id": 1,
            "name": "Spicy Zinger",
            "protein": 28,
            "restaurant_id": 1,
            "sodium": 900,
            "total_carbs": 48,
            "total_fat": 19
        },
        {
            "calories": 840,
            "cholesterol": 165,
            "id": 2,
            "name": "Cheeseburger",
            "protein": 47,
            "restaurant_id": 2,
            "sodium": 1050,
            "total_carbs": 40,
            "total_fat": 55
        },
        {
            "calories": 240,
            "cholesterol": 25,
            "id": 3,
            "name": "Caramel Macchiato",
            "protein": 10,
            "restaurant_id": 3,
            "sodium": 130,
            "total_carbs": 34,
            "total_fat": 7
        },
        {
            "calories": 1000,
            "cholesterol": 195,
            "id": 4,
            "name": "Burrito",
            "protein": 60,
            "restaurant_id": 4,
            "sodium": 1855,
            "total_carbs": 104,
            "total_fat": 39
        }
    ],
    "success": true
}
```

#### GET '/restaurants/<int:restaurant_id>/orders'
- Fetches the list of orders for the restaurant with id `restaurant_id`
- Required Permission: `get:orders`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/restaurants/3/orders
```

```
EXAMPLE RETURN

{
    "orders": [
        {
            "calories": 240,
            "cholesterol": 25,
            "id": 3,
            "name": "Caramel Macchiato",
            "protein": 10,
            "restaurant_id": 3,
            "sodium": 130,
            "total_carbs": 34,
            "total_fat": 7
        }
    ],
    "success": true
}
```

#### POST '/restaurants'
- Adds a restaurant from the provided request body to the database
- Required Permission: `post:restaurants`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/restaurants
```

``` 
EXAMPLE REQUEST BODY

{
    "name": "Cheesecake Factory",
    "cuisine": "American"
}
```

```
EXAMPLE RETURN

{
    "restaurants": [
        {
            "cuisine": "American",
            "id": 5,
            "name": "Cheesecake Factory"
        }
    ],
    "success": true
}
```

#### POST '/orders'
- Adds an order from the provided request body to the database
- Required Permission: `post:orders`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/orders
```

``` 
EXAMPLE REQUEST BODY

{
    "name": "White Chocolate Raspberry Truffle Cheesecake (Slice)",
    "calories": 929,
    "cholesterol": 31,
    "protein": 9,
    "restaurant_id": 5,
    "sodium": 370,
    "total_carbs": 85,
    "total_fat": 39
}
```

```
EXAMPLE RETURN

{
    "orders": [
        {
            "calories": 929,
            "cholesterol": 31,
            "id": 5,
            "name": "White Chocolate Raspberry Truffle Cheesecake (Slice)",
            "protein": 9,
            "restaurant_id": 5,
            "sodium": 370,
            "total_carbs": 85,
            "total_fat": 39
        }
    ],
    "success": true
}
```

#### PATCH '/restaurants/<int:restaurant_id>'
- Updates the info of restaurant with id `restaurant_id` using the provided request body
- Required Permission: `patch:restaurants`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/restaurants/5
```

``` 
EXAMPLE REQUEST BODY

{
    "name": "The Cheesecake Factory"
}
```

```
EXAMPLE RETURN

{
    "restaurants": [
        {
            "cuisine": "American",
            "id": 5,
            "name": "The Cheesecake Factory"
        }
    ],
    "success": true
}
```

#### PATCH '/orders/<int:order_id>'
- Updates the info of order with id `order_id` using the provided request body
- Required Permission: `patch:orders`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/orders/5
```

``` 
EXAMPLE REQUEST BODY

{
    "protein": 11,
    "cholesterol": 33
}
```

```
EXAMPLE RETURN

{
    "orders": [
        {
            "calories": 929,
            "cholesterol": 33,
            "id": 5,
            "name": "White Chocolate Raspberry Truffle Cheesecake (Slice)",
            "protein": 11,
            "restaurant_id": 5,
            "sodium": 370,
            "total_carbs": 85,
            "total_fat": 39
        }
    ],
    "success": true
}
```

#### DELETE '/restaurants/<int:restaurant_id>'
- Deletes the restaurant with id `restaurant_id` from the database
- Required Permission: `delete:restaurants`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/restaurants/6
```

```
EXAMPLE RETURN

{
    "delete": 6,
    "success": true
}
```

#### DELETE '/orders/<int:order_id>'
- Deletes the order with id `order_id` from the database
- Required Permission: `delete:orders`
- Returns: A JSON with keys as per the example

``` 
EXAMPLE REQUEST URL

http://localhost:5000/orders/6
```

```
EXAMPLE RETURN

{
    "delete": 6,
    "success": true
}
```

## Testing
To run the tests, execute the following on your terminal:
```
dropdb test_nutrition
createdb test_nutrition
python test_app.py
```