import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.host = 'localhost:5432'
        self.username = 'postgres'
        self.password = '1234'
        self.database_path = f"postgres://{self.username}:{self.password}@{self.host}/{self.database_name}"
        
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''------------------------------------------------------------------------------------------
    test endpoint to handle GET requests for all available categories
    ------------------------------------------------------------------------------------------''' 
    def test_categories_get_success(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['success'], True)

    '''------------------------------------------------------------------------------------------
    test endpoint to handle GET requests for questions, including pagination (every 10 questions)
    ------------------------------------------------------------------------------------------'''
    def test_questions_get_success(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 'all')

    def test_questions_get_failure(self):
        response = self.client().get('/questions?page=3')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    '''------------------------------------------------------------------------------------------
    test GET endpoint to get questions based on category
    ------------------------------------------------------------------------------------------'''
    def test_questions_get_by_category_success(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_questions_get_by_category_failure(self):
        response = self.client().get('/categories/7/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    '''------------------------------------------------------------------------------------------
    test endpoint to DELETE question using a question ID
    ------------------------------------------------------------------------------------------'''
    def test_questions_delete_success(self):
        response = self.client().delete('/questions/6')
        data = json.loads(response.data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['success'])

    
    def test_questions_delete_failure(self):
        response = self.client().delete('/questions/6234')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    '''------------------------------------------------------------------------------------------
    test endpoint to POST a new question
    ------------------------------------------------------------------------------------------'''
    def test_questions_post_success(self):
        question = 'Which german city has the largest population?'
        answer = 'Berlin'
        response = self.client().post(
            '/questions',
            content_type='application/json',
            data=json.dumps({
                'question': question,
                'answer': answer,
                'difficulty': 1,
                'category': 3
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['question'], question)
        self.assertEqual(data['data']['answer'], answer)

    def test_questions_post_failure(self):
        question = 'Which german city has the largest population?'
        answer = 'Berlin'
        response = self.client().post(
            '/questions',
            content_type='application/json',
            data=json.dumps({
                'question': '',
                'answer': answer,
                'difficulty': 1,
                'category': 3
            })
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad Request')
    
    '''------------------------------------------------------------------------------------------
    test POST endpoint to get questions based on a search term
    ------------------------------------------------------------------------------------------'''
    def test_questions_search_success(self):
        response = self.client().post(
            '/questions',
            content_type='application/json',
            data=json.dumps({
                'searchTerm': 'autobiography'
            }))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_questions_search_failure(self):
        response = self.client().post(
            '/questions',
            content_type='application/json',
            data=json.dumps({
                'searchTerm': 'xyz'
            }))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

    '''------------------------------------------------------------------------------------------
    test POST endpoint to get questions to play the quiz
    ------------------------------------------------------------------------------------------'''
    def test_questions_get_for_quiz_success(self):
        response = self.client().post(
            '/quizzes',
            content_type='application/json',
            data=json.dumps({
                'previous_questions':[17,18],
                'quiz_category':{
                    'type': 'Art',
                    'id': 2
                }
            }))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['question']))

    def test_questions_get_for_quiz_failure(self):
        response = self.client().post(
            '/quizzes',
            content_type='application/json',
            data=json.dumps({
                'previous_questions':[10,11],
                'quiz_category':{
                    'type': 'Sports',
                    'id': 6
                }
            }))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not Found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()