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
        self.database_path = os.getenv('DB_TEST_URI')
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

    # TESTS FOR CATEGORIES

    def test_get_categories_successful(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']), 6)

    # TESTS FOR QUESTIONS

    def test_get_questions_successful(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(len(data['questions']), 10)

    def test_get_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_questions_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 2)

    def test_search_questions_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'zblut'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    def test_create_question_successful(self):
        res = self.client().post('/questions', json={
            "question": 'What is the capital of France?',
            "answer": 'Paris',
            "difficulty": 1,
            "category": Category.query.filter(Category.type == 'Geography')
            .one().id
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIs(type(data['created']), int)
        self.assertGreater(len(data['questions']), 0)
        self.assertGreater(data['total_questions'], 0)

    def test_create_question_with_wrong_category(self):
        res = self.client().post('/questions', json={
            "question": 'What is the capital of France?',
            "answer": 'Paris',
            "difficulty": 1,
            "category": 3839
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_question_successful(self):
        res = self.client().delete('/questions/23')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 23)

    def test_delete_question_incorrect_id(self):
        res = self.client().delete('/questions/320')

        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category_successful(self):
        current_category = 3
        res = self.client().\
            get('/categories/' + str(current_category) + '/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], current_category)
        self.assertTrue(data['total_questions'])
        self.assertLessEqual(len(data['questions']), 10)

    def test_get_questions_by_category_beyond_valid_page(self):
        current_category = 3
        page = 10000

        res = self.client().get('/categories/' + str(current_category) +
                                '/questions?page=' + str(page))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_wrong_category(self):
        current_category = 3000
        page = 1

        res = self.client().get('/categories/' + str(current_category) +
                                '/questions?page=' + str(page))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_play_quizz_successful(self):
        res = self.client().post('/quizz', json={
            "previous_questions": [],
            "quiz_category": Category.query.
            filter(Category.type == 'Geography').one().id
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_play_quizz_404_no_category(self):
        res = self.client().post('/quizz', json={
            "previous_questions": [],
            "category": 39201
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
