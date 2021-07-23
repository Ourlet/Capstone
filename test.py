import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

class capstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.director_token = os.environ['director_token']
        self.producer_token = os.environ['producer_token']
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.VALID_POST_ACTOR = {
            "id" : 1,
            "name": "Gerard Depardieu",
            "age": 88,
            "gender": "M"
        }

        self.INVALID_POST_ACTOR = {
            "name": "Gerard Depardieu",
        }

        self.VALID_PATCH_ACTOR = {
            "age": 88,
        }

        self.VALID_PATCH_MOVIE = {
            "title": "Terminator"
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

    def test_api_call_no_token(self):
        """Failing Test trying to make a call with no token"""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_get_movies(self):
        """Passing Test for GET /movies"""
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
    
    def test_get_actors(self):
        """Passing Test for GET /actors"""
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('actors', data)

    def test_create_actor(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.VALID_POST_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_update_movie(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.VALID_PATCH_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
       
    def test_delete_actor_with_producer_token(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/3', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_404_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/1000', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()