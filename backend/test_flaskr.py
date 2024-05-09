import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.database_name = os.getenv("DB_NAME_TEST")
        self.database_url = os.getenv("DB_URL")
        self.database_path = "postgres://{}/{}".format(self.database_url, self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_question = {"question":"Country of origin for MilkMocha", "answer":"Indonesia", "category":"5", "difficulty":"2"}
        self.success_quiz = {"previous_questions": [6, 24, 2], "quiz_category": {"type": "Entertainment", "id": "5"}}
        self.error_quiz = {"previous_questions": [], "quiz_category": {}}


    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_fail_get_questions(self):
        res = self.client().get('/questions?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_delete_question(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 4).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)
        self.assertEqual(question, None)

    def test_fail_delete_book(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'],"Succesfully created question")

    def test_search_question(self):
        res = self.client().post('/questions', json={"searchTerm": "peanut butter"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fail_search_question(self):
        res = self.client().post('/questions', json={"searchTerm": "dummy"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['totalQuestions'], 4)
        self.assertEqual(data['currentCategory'], 'Art')

    def test_fail_get_question_by_category(self):
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_get_quiz(self):
        res = self.client().post('/quizzes', json=self.success_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['question'], None)
        
    def test_fail_get_quiz(self):
        res = self.client().post('/quizzes', json=self.error_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()