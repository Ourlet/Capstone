import os
import json
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import *
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    @app.route('/actors', methods=["GET"])
    @requires_auth('get:actors')
    def get_actors(payload):
        
        actors = Actor.query.order_by(Actor.id).all()

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.actors() for actor in actors]
        }), 200

    
    @app.route('/movies', methods=["GET"])
    @requires_auth('get:movies')
    def get_movies(payload):

        movies = Movie.query.order_by(Movie.id).all()

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.list_movie_with_actors() for movie in movies]
        }), 200

    
    @app.route('/actors/<int:id>', methods=["DELETE"])
    @requires_auth('delete:actor')
    def delete_actors(payload,id):

        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        

        actor.delete()

        return jsonify({
            'success': True,
            'delete actor': actor.id
        })
    
    '''
    curl -X DELETE http://127.0.0.1:5000/actors/5 -H "Accept: application/json"    
    '''
    
    @app.route('/movies/<int:id>', methods=["DELETE"])
    @requires_auth('delete:movie')
    def delete_movies(payload,id):

        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        
        movie.delete()

        return jsonify({
            'success': True,
            'delete movie': movie.id
        })  

    '''
    curl -X DELETE http://127.0.0.1:5000/movies/4 -H "Accept: application/json"
    '''

    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actor')
    def add_actors(payload):

        body = request.get_json()
        
        try:
            if 'name' and 'gender' and 'age' not in body:
                abort(422)

            name = body['name']
            gender = body['gender']
            age = body['age']

            actor = Actor(name = name, gender = gender, age = age)
            actor.insert()
        
        except:
            abort(400)

        return jsonify ({
            'success' : True,
            'actor': [actor.actors()]
        })

    '''
    curl --header "Content-Type: application/json" --request POST --data '{"name":"Camelia Jordana","age":"31", "gender":"F"}' http://127.0.0.1:5000/actors
    '''

    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movie')
    def add_movies(payload):

        body = request.get_json()

        try:
            if 'title' and 'release_date' not in body:
                abort(422)

            title = body['title']
            release_date = body['release_date']

            movie = Movie(title = title, release_date = release_date)

            movie.insert()
        
        except:
            abort(400)

        return jsonify ({
            'success': True, 
            'movie' : [movie.list_movie()]
        })
    
    '''
    curl --header "Content-Type: application/json" --request POST --data '{"title":"Curiosa","release_date":"2019-04-03"}' http://127.0.0.1:5000/movies
    '''

    @app.route('/actors/<int:id>', methods=["PATCH"])
    @requires_auth('patch:actor')
    def patch_actors(payload,id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        
        body = request.get_json()

        try:
            if 'name' in body:
                actor.name = body['name']

            if 'gender' in body:
                actor.gender = body['gender']

            if 'age' in body:
                actor.age = body['age']
            
            actor.update()
       
        except:
            abort(422)

        return jsonify({
            'success': True, 
            'actor': [actor.actors()]
        })
    
    '''
    curl -X PATCH http://127.0.0.1:5000/actors/1 -H "Content-Type: application/json" -H "Accept: application/json" --data '{"age":"61"}' 
    '''

    @app.route('/movies/<int:id>', methods=["PATCH"])
    @requires_auth('patch:movie')
    def patch_movies(payload,id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        body = request.get_json()

        try:
            if 'title' in body:
                movie.title = body['title']

            if 'release_date' in body:
                movie.release_date = body['release_date']

            movie.update()

        except:
            abort(422)

        return jsonify({
            'success': True,
            'movie': [movie.list_movie()]
        })
    
    '''
    curl -X PATCH http://127.0.0.1:5000/movies/1 -H "Content-Type: application/json" -H "Accept: application/json" --data '{"title":"The Expendables 2"}'
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        "success": False,
                        "error": 400,
                        "message": "bad request"
                        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
                        "success": False,
                        "error": 401,
                        "message": "Unauthorized "
                        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
                        "success": False,
                        "error": 403,
                        "message": "forbidden"
                        }), 403

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app

app = create_app()

if __name__ == '__main__':
    app.run()