# Full Stack Trivia API Backend

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

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb -U <username> trivia
psql -f trivia.psql trivia <username>
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
$env:FLASK_APP=flaskr
$env:FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

### Endpoints

#### View Categories
```
GET '/categories'
```
- Fetches a json object of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

Example: ```curl.exe 'http://localhost:5000/categories'```

Response data:
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true
}
```

#### View Questions
```
GET '/questions'
```
- Fetches a json object with the following keys: 
    - categories: A list of category objects, where each object contains a dictionary with the keys id and type.
    - questions: A list of questions objects,  where each object contains a dictionary with the keys question, answer, category, difficulty.
    - total questions: An integer representing the total number of questions in the database.
    - current category: This defaults to 'all' for this route.
- Request Arguments:
    - page: An integer that represents the requested page. It is optional and defaults to 1.
    - max: An integer that represents the maximum number of questions per page. It is optional and defaults to 10.
    
Example: ```curl.exe 'http://localhost:5000/questions?page=2&max=5'```

Response data:
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "current_category": "all", 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

#### Delete a Question
```
DELETE '/questions/<int:id>'
```
- Deletes a certain question from the database by the id specified in the url
- If no question in the database matches the id, a 404 error is returned

Example: ```curl.exe -X DELETE 'http://localhost:5000/questions/6'```

Response data:
```
{
    'success': True,
    'message': 'Successfully deleted question #6'
}
```
#### Add or Search for a Question
```
POST '/questions'
```
The questions-endpoint in combination with the POST-method serves for adding a question or searching for a question depending on provided data.

##### Add a question
- Inserts a question into the database by taking a jason object with the mandatory fields question, answer, category and difficulty.
- It returns a json object with the entered data and if it was succesfull.

Example for adding a question: ```curl.exe -X POST 'http://localhost:5000/questions' -d '{"\""question"\"": "\""What is the air-speed velocity of an unladen swallow?"\"", "\""answer"\"": "\""An African or European swallow?"\"", "\""category"\"": 5, "\""difficulty"\"": 1}' -H 'Content-Type: application/json'```

Request body:
```
{
  "question": "What is the air-speed velocity of an unladen swallow?", 
  "answer": "An African or European swallow?", 
  "category": 5, 
  "difficulty": 1
}
```

Response data:
```
{
  "data": {
    "answer": "An African or European swallow?",
    "category": 5,
    "difficulty": 1,
    "id": 25,
    "question": "What is the air-speed velocity of an unladen swallow?"
  },
  "success": true
}
```

##### Search for a question
- This endpoint performs a case insensitive search based on a provided search term.
- It returns a json object with the following keys:
  - current_category: defaults to null
  - questions: A list of questions objects,  where each object contains a dictionary with the keys question, answer, category, difficulty.
  - total_questions: total number of questions found containing the search term

Example for searching a question: ```curl.exe -X POST 'http://localhost:5000/questions' -d '{"\""searchTerm"\"": "\""swallow"\""}' -H 'Content-Type: application/json'```

Request body:
```
{
  "searchTerm": "swallow"
}
```

Response data:
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "An African or European swallow?",
      "category": 5,
      "difficulty": 1,
      "id": 25,
      "question": "What is the air-speed velocity of an unladen swallow?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### View Questions by Category
```
GET '/categories/<int:id>/questions'
```
- Fetches a dictionary with the following keys: 
    - current_category: A dictionary of the current category with the keys id and type.
    - questions: A list of questions objects,  where each object contains a dictionary with the keys question, answer, category, difficulty.
    - total questions: An integer representing the total number of questions in the database.

Example: ```curl.exe http://localhost:5000/categories/5/questions```

Response data:
```
{
  "current_category": {
    "id": 5,
    "type": "Entertainment"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

#### Play the Quiz
```
POST '/quizzes'
```
- Fetches a json object based on category and previous questions with the following keys: 
    - question: A dictionary with the keys question, answer, category, difficulty.

Example: ```curl.exe -X POST 'http://localhost:5000/quizzes' -d '{"\""previous_questions"\"": [1, 11], "\""quiz_category"\"": {"\""id"\"": 3, "\""type"\"": "\""Geography"\""}}' -H 'Content-Type: application/json'```

Request body:
```
{
  "previous_questions": [1, 11], 
  "quiz_category": {
    "id": 3, 
    "type": "Geography"
  }
}
```

Response data:
```
{
  "question": {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
  "success": true
}
```

### Error Handling
- Occuring errors are returned as json objects with the following format.
- The API can return the following errors:
  - 400 Bad Request
  - 404 Not Found
  - 422 Unprocessable Entity
  - 500 Internal Server Error

Response data:
```
{
    'success': False,
    'error': 400,
    'message': 'Bad Request'
}
```


### Testing
To run the tests, navigate to the backend directory and execute the following commands:
``` bash
dropdb -U <username> trivia_test
createdb -U <username> trivia_test
psql -f trivia.psql trivia_test <username>
python test_flaskr.py
```
