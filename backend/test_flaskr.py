import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from tweak import DB_NAME, DB_USER, DB_PASSWORD

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(DB_USER,DB_PASSWORD,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.question = {
            'question': 'Who was the greatest boxer?',
            'answer': 'Muhammad Ali',
            'difficulty': 2,
            'category': 3
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data)

    def test_fetch_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])

    def test_404_get_page_not_found(self):
        res = self.client().get('/questions?page=25')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(len(data), 3)

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_question(self):
        res = self.client().post('/question', json=self.question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_422_unprocessable_entity(self):
        res = self.client().delete('/questions/50')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Page or Question not Found')


    def test_404_question_not_found(self):
        res = self.client().post('/questions/searchedTerm?category=15', json={'searchTerm': 'wh'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data)

    def test_search_question(self):
        res = self.client().post('/questions/searchedTerm?category=4', json={'searchTerm': 'w'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))

    
    def test_get_category_question(self):
        res = self.client().get('/categories/2/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['current_category'], 2)

    def test_404_category_not_found(self):
        res = self.client().get('/categories/18/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertNotEqual(data, None)
        self.assertEqual(data['message'], 'Page or Question not Found')

    def test_fetch_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [],
         'quiz_category': {'type': 'Art', 'id': 2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 2)

    def test_404_quiz_question_not_found(self):
        res = self.client().post('/quizzes',
         json={'previous_questions': [17, 20], 'quiz_category': 13})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()