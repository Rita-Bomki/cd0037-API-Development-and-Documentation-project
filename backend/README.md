# Getting Started

Trivia App is knowledge based app where students could engage themselve in searching questions, add question, and also delete questions organized in categories.

## Base URL

**Frontend:  http://localhost:3000/**

**Backend: http://127.0.0.1:5000/**

___


# Guideline
```
  Kindly follow the PEP18-STYLE
  Follow the collection/item/collection for the Routes
```



___
### Prerequisite & Installation
  **Virtual Environment**
    
  Linux/Mac
      
      $ python -m venv ritaenv
      $ source ritaenv/bin/activate


  To deactivate the Virtual Environment

      $ deactivate

  **Backend**
      
      Note: Ensure you are are in the backend directory

  >pip installations
      
      $ pip3 install -r > requirements.txt

  **Database Creation**
  
  Populate your table with trivia.psql 

      $ createdb trivia
      $ psql trivia < trivia.psql


  **Starting Server**

      $ export FLASK_APP=flaskr
      $ export FLASK_DEBUG=True
      $ flask run --reload


  **Frontend**

  > Make sure you are within the /frontend/src directory

      $ npm install
      $ npm start


___
  
# Testing
> Ensure you are within the /backend directory
  
  Database creation

      $ createdb trivia_test
      $ psql trivia_test < trivia.psql

  Starting Server

      $ python test_flaskr.py


# Error Handling

  Error response is in json form, including the success, error type and and their error message.

      Sample Resource

      {
        'success': False,
        'error': 404,
        'message': 'Page not found'
      }

Errors:
   
   1. **404** : Page not found
   2. **400** : Bad request
   3. **500** : Internal Server Error
   4. **422** : Unprocessable Entity
   5. **405** : Bad Method


# API REFERENCES

`GET /categories`
  
  
  - Fetch categories as dictionary with key and value of corresponding category string
  - Request Argument: None
  - Returns: Key-Value representation of id and string of each category

**Sample Response**
```json
{
  "categories": {
    '1': 'Science',
    '2': 'Art',
    '3': 'Geography',
    '4': 'History',
    '5': 'Entertainment',
    '6': 'Sports'
  }
}

```

`GET /questions`

**General**
  
  - Fetch total questions
  - Request Argument: page =>  Integer
  - Returns: A paginated list of questions

**Sample Response**
```json
{
  "questions": [
      {
        "id": 1,
        "question": "What Blockchain?",
        "answer": "A cryptographic oriented database interlocked together by block",
        "difficulty": 3,
        "category": 4
      },
  ],
  "totalQuestion": 17,
  "category": {
    '1': 'Science',
    '2': 'Art',
    '3': 'Geography,
    '4': 'History,
    '5': 'Entertainment',
    '6': 'Sports',
  },
  'currentCategory': 3
}
```

`DELETE /questions/${question_id}

**General**

- Delete Question based on the question id
- Request Argument: question_id : int
- Returns: A json value with success and message

Sample Request
```bash
  curl -X DELETE http://localhost:5000/questions/10
```

Sample Response

      {
        'success': True,
        'message': OK
      }



  `POST /questions`
  **General**
  
  - Sends request that add question to trivia database
  - Request Argument: None
  - Request body:

        {
          'question': "Who's donald trump",
          'answer': "America President",
          'category': 3,
          'difficulty': 4
        }
  - Return: A json with success equal to True
  
  Sample Response


        {
          'success': True
        }


`POST /questions/searchedTerm

**General**

- Get question based on the searchTerm in the request body
- Request Argument: SearchTerm : String
- Request Body: 

      {
          'searchTerm': 'what'
      }

- Returns: Matched question, current category and total questions

Sample Response

      {
          'questions': [
            {
              'queston': "What country is the world power",
              'answer': "United State of America",
              'category': 2,
              'difficulty': 1
            }
          ],
          'total_questions': 3,
          'current_Category': 2,
      }


`GET /categories/${id}/questions?page=${page_no}`

**General**

- Fetches paginated questions based on categories
- Request Arguent: category_id, page : integers
- Returns: A question that matches the category id, the current category and total questions count
  
Sample Response
      
      {
        'questions': [
        {
          'question': 'Who is Marie Curie',
          'answer': 'The mother of Radioactivity',
          'category': 3,
          'difficulty' 4
        },
        {
          'question': 'Who is the founder of Facebook',
          'answer': 'Mark Zuckerberg',
          'category': 3,
          'difficulty': 2
        }
      ],
      'total_questions': 2,
      'current_category': 3
      }


`POST /quizzes`
**General**

- retrieve a question that's not has yet been shown or whose id is not in the previous questions list
- Request Argument: quiz_category : integer, previous_question: list
- Request Body:
  
      {
        'quiz_category': 2,
        'previous_questions': [4, 5, 7]
      }

- Returns: A question dictionary and list of previous questions

Sample Response

    {
      'question': {
        'id': 4,
        'question': 'Who is the Greatest footballer?',
        'answer': 'Lionel Messi',
        'category': 4,
        'difficulty': 2
      },
      'previousQuestions': [3, 2, 17]
    }



## Authors
1. Rita Bomki