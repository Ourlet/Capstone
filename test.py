import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.VALID_POST_ACTOR = {
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

        self.INVALID_PATCH_ACTOR = {}

        self.VALID_POST_MOVIE = {
            "title": "Jurassic Park",
            "release_date": "2001-04-16"
        }

        self.INVALID_POST_MOVIE = {
            "title": "Twilight",
        }

        self.VALID_PATCH_MOVIE = {
            "title": "Terminator"
        }

        self.INVALID_PATCH_MOVIE = {}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
            """Executed after reach test"""
            pass

    

