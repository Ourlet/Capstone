import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
    
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    
    """ uncomment at the first time running the app """
    
    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()