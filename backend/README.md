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

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## API Documentation
* GET "/categories"
    - Fetches a dictionary of categories in which id is the key, and type is the value
    - Request Parameters: None
    - Response Body:
    
    `categories`: Dictionary of *Category ID*:*Category Type*
```json
{
  "categories": {
    "1": "Science",
    "2": "Art"
  } 
}
```

* POST "/categories"
    - Adds a new category to the database
    - Request Body:
    
    `type`: The Category's type
    - Response Body:
    
    `created`: Created category ID

    `categories`: List of all categories, including the created one

    `total_categories`: Number of questions after addition
```json
{
  ""
}

* GET "/questions?page=1"
    - Fetches the questions to be displayed on the page using page number
    - Request Parameters: `page`: Page number (optional, defaults to 1)
    - Response Body:

    `questions`: List of questions

    `categories`: Dictionary of *Category ID*:*Category Type*

    `total_questions`: Total number of  questions
```json
{
  "questions": [{
    "id": 5, 
    "answer": "Maya Angelou", 
    "category": 2, 
    "difficulty": 2, 
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  }],
  "categories": {
    "1": "Science",
    "2": "Art"
  },
  "total_questions": 1
}
```

* DELETE "/questions/<int:question_id>"
    - Deletes a question from the database
    - Request Parameters: `question_id`: ID of the question to delete
    - Response Body:

    `deleted`: Deleted question's ID
    `total_questions`: Number of questions remaining after deletion
```json
{
  "deleted": 20,
  "total_questions": 19
}
```

* POST "/questions"
    - Adds a new question to the database
    - Request Body:
    
    `question`: Question text
    
    `answer`: Answer text
    
    `category`: Category ID
    
    `difficulty`: Difficulty Level
    - Response Body:
    
    `created`: Created question ID

    `total_questions`: Number of questions after addition
```json
{
  "question": {
    "id": 14, 
    "answer": "The Palace of Versailles", 
    "category": 3, 
    "difficulty": 3, 
    "question": "In which royal palace would you find the Hall of Mirrors?"
  }
}
```

* POST "/search"
    - Fetches questions based on a submitted search query
    - Request Body:
    
    `searchTerm`: Search term
    - Response Body:
    
    `questions`: List of questions found for which the question attribute contains the searchTerm
    
    `total_questions`: Total number of questions
```json
{
  "questions": [{
    "id": 14, 
    "answer": "The Palace of Versailles", 
    "category": 3, 
    "difficulty": 3, 
    "question": "In which royal palace would you find the Hall of Mirrors?",
    ...
  }],
  "total_questions": 3
}
```

* GET "/categories/<int:category_id>/questions"
    - Fetches questions for a specified category
    - Request Parameters: `category_id`: Category ID
    - Response Body:

    `questions`: List of questions for which the category attribute corresponds to the requested category ID

    `total_questions`: Total number of questions for this category
    
    `current_category`: Current category ID
```json
{
  "questions": [{
    "id": 14, 
    "answer": "The Palace of Versailles", 
    "category": 3, 
    "difficulty": 3, 
    "question": "In which royal palace would you find the Hall of Mirrors?",
    ...
  }],
  "total_questions": 3,
  "current_category": 3
}
```

* POST "/quizz"
    - Fetches a unique question for a said category
    - Request Body:
    
    `previous_questions`: List of previously answered questions (the returned question cannot be one on those)

    `quiz_category`: Category for the quiz to be made on (if set to 0, no specific category will be applied)
    - Response Body:
    
    `question`: Random question from the requested category
```json
{
  "question": {
    "id": 14, 
    "answer": "The Palace of Versailles", 
    "category": 3, 
    "difficulty": 3, 
    "question": "In which royal palace would you find the Hall of Mirrors?",
    ...
  }
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```