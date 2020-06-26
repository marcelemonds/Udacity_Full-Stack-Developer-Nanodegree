# Capstone Project: Casting Agency

## Motivation for the project

This project serves the purpose to show that the lessons learned during the Full Stack Web Developer Nanodegree were fully understood and can all be implemented in one project.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
$env:FLASK_APP = "app.py"
$env:FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` from the main directory.

### Test Deployment
For testing purposes the api is hosted via Heroku. For the deployment Heroku is looking for the following files in the directory:
- `requirements.txt`: A list with all the dependencies to run the api.
- `Procfile`: The file contains information about the webserver and api.
- `setup.sh`: The file contains all the needed environment variables (e.g. for Auth0 or the api itself)
- `manage.py`: Instructions for Heroku about how to run database migrations.

### Roles
The Authorization is setup via Auth0 and accepts permissions from the following roles:

Casting Assistent:
- can view actors: `get:actors`
- can view movies: `get:movies`

Casting Director:
- all permissions a casting assistent has and...
- add new actors: `post:actors`
- delete existing actors: `delete:actors`
- edit existing actors: `patch:actors`
- edit existing movies: `patch:movies`

Executive Producer:
- all permissions a casting dirctor has and...
- add new movies: `post:movies`
- delete existing movies: `delete:movies`

The needed permission is checked for each route.

Here are example logins for the roles mentioned above:
- castingassistant@fsndwebapp.com
- castingdirector@fsndwebapp.com
- executiveproducer@fsndwebapp.com

### Endpoints

The API ist hosted live via Heroku and be accessed via `https://capstonemarcel.herokuapp.com/api/`. Tokes to use for testing purposes can befound in `test_api.py`.

#### Login to Auth0
```
GET '/api/login'
```
- redirects to Auth0s' login page
- response: a json object with keys success and token

Response data:
```
{
    "success": True,
    "token": "example_token"
}
```

####3 Logout from Auth0
```
GET '/api/logout'
```
- logs out the current user from Auth0
- redirects to the login page

#### View Actors
```
GET '/api/actors
PERMISSION get:actors
```
- fetches a list of actors in a json object
- request arguments: none
- response: a json object with keys success and actors

Example: ```curl.exe 'http://localhost:5000/api/actors' -H 'Authorization: Bearer <Token>'```

Response data:
```
{
    "actors": [
        {
            "id": 1,
            "name": "Mr. Creosote", 
            "age": 45, 
            "gender": "male"
        },
        {
            "id": 2,
            "name": "Roger the Shrubber",
            "age": 35,
            "gender": "male"
        }
    ],
    "success": True
}
```

#### Add a new Actor
```
POST '/api/actors
PERMISSION post:actors
```
- Inserts an actor into the database by taking a json object with the mandatory fields name, age and gender.
- It returns a json object with the entered data and if it was succesfull.

Example: ```curl.exe -X POST 'http://localhost:5000/api/actors' -d '{"\""name"\"": "\""Mr. Creosote"\"", "\""age"\"": 45, "\""gender"\"": "\""male"\""}' -H 'Content-Type: application/json' -H 'Authorization: Bearer <Token>'```

Request body:
```
{
    "name": "Mr. Creosote", 
    "age": 45, 
    "gender": "male"
}
```

Response data:
```
{
    "actor": {
        "id": 1,
        "name": "Mr. Creosote", 
        "age": 45, 
        "gender": "male"
        },
    "success": true
}
```

#### Edit an existing Actor
```
PATCH '/api/actors
PERMISSION patch:actors
```
- Edits an actor in the database by taking a json object with the optional fields name, age and gender.
- It returns a json object with the edited actor and if it was succesfull.

Example: ```curl.exe -X PATCH 'http://localhost:5000/api/actors/1' -d '{"\""age"\"": 46}' -H 'Content-Type: application/json' -H 'Authorization: Bearer <Token>'```

Request body:
```
{
    "age": 48
}
```

Response data:
```
{
    "actor": {
        "id": 1,
        "name": "Mr. Creosote", 
        "age": 48, 
        "gender": "male"
        },
    "success": true
}
```


#### Delete an existing Actor
```
DELETE '/api/actors/<int:id>'
PERMISSION delete:actors
```

- Deletes a certain actor from the database by the id specified in the url
- If no actor in the database matches the id, a 404 error is returned

Example: ```curl.exe -X DELETE 'http://localhost:5000/api/actors/1' -H 'Authorization: Bearer <Token>'```

Response data:
```
{
    'success': True,
    'delete': 1
}
```

#### View Movies
```
GET '/api/movies
PERMISSION get:movies
```
- fetches a list of movies in a json object
- request arguments: none
- response: a json object with keys success and movies

Example: ```curl.exe 'http://localhost:5000/api/actors' -H 'Authorization: Bearer <Token>'```

Response data:
```
{
    "movies": [
        {
            "id": 1,
            "title": "The Meaning of Life", 
            "release_date": "1983-03-31"
        },
        {
            "title": "The Holy Grail", 
            "release_date": "1975-04-03"
        }
    ],
    "success": True
}
```

#### Add a new Movie
```
POST '/api/movies
PERMISSION post:movies
```
- Inserts an movie into the database by taking a json object with the mandatory fields title and release_date.
- It returns a json object with the entered data and if it was succesfull.

Example: ```curl.exe -X POST 'http://localhost:5000/api/actors' -d '{"\""title"\"": "\""The Meaning of Life"\"","\""release_date"\"": "\""1983-03-31"\""}' -H 'Content-Type: application/json' -H 'Authorization: Bearer <Token>'```

Request body:
```
{
  "title": "The Meaning of Life", 
  "release_date": "1983-03-31"
}
```

Response data:
```
{
    "movie": {
        "id": 1,
        "title": "The Meaning of Life", 
        "release_date": "1983-03-31"
        },
    "success": true
}
```

#### Edit an existing Movie
```
PATCH '/api/movies
PERMISSION patch:movies
```
- Edits a movie in the database by taking a json object with the optional fields title and release_date.
- It returns a json object with the edited movie and if it was succesfull.

Example: ```curl.exe -X PATCH 'http://localhost:5000/api/movies/2' -d '{"\""title"\"": "\""Monty Python and the Holy Grail"\""}' -H 'Content-Type: application/json' -H 'Authorization: Bearer <Token>'```

Request body:
```
{
    "title": "Monty Python and the Holy Grail"
}
```

Response data:
```
{
    "actor": {
        "id": 2,
        "title": "Monty Python and the Holy Grail", 
        "release_date": "1975-04-03"
        },
    "success": true
}
```

#### Delete an existing Movie
```
DELETE '/api/movies/<int:id>'
PERMISSION delete:movies
```

- Deletes a certain movie from the database by the id specified in the url
- If no movie in the database matches the id, a 404 error is returned

Example: ```curl.exe -X DELETE 'http://localhost:5000/api/movies/1' -H 'Authorization: Bearer <Token>'```

Response data:
```
{
    'success': True,
    'delete': 1
}
```

### Testing
To run the tests, navigate to the backend directory and execute the following commands:
``` bash
dropdb -U <username> capstone
createdb -U <username> capstone
python test_api.py
```
