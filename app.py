import click
import json
import os
import unittest
import sys

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import Actor, Movie, setup_db
from auth import requires_auth, AuthError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # CORS app
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )
        return response

    ## ROUTES
    # this for get all actors
    @app.route('/actors')
    @requires_auth('read: actors')

    def get_actors(token):
        actors = Actor.query.all()
        if not actors:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route('/movies')
    @requires_auth('read:movies')
    def get_movies(token):
        movies = Movie.query.all()
        if not movies:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(token):
        try:
            body = request.get_json()
            actor = Actor(
                name=body.get('name'),
                age=body.get('age'),
                gender=body.get('gender'),

            )
            actor.insert()

            return jsonify({
                'success': True,
                'actors': actor.format()
            }), 200
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(token):
        try:
            body = request.get_json()
            movie = Movie(
                title=body.get('title'),
                release_date=body.get('release_date'),

            )
            movie.insert()

            return jsonify({
                'success': True,
                'actors': movie.format()
            }), 200
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor_submission(token, actor_id):
        try:
            body = request.get_json()
            actor = Actor.query.get(actor_id)
            if not actor:
                abort(404)
            actor.name = body.get('name')
            actor.age = body.get('age')
            actor.gender = body.get('gender')

            actor.update()

        except:
            print(sys.exc_info())
            abort(422)

        return jsonify({
            'success': True,
            'actors': [actor.format()]
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies_submission(token, movie_id):
        try:
            body = request.get_json()
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(404)
            movie.title = body.get('title')
            movie.release_date = body.get('release_date')

            movie.update()

        except:
            print(sys.exc_info())
            abort(422)

        return jsonify({
            'success': True,
            'movies': [movie.format()]
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(token, actor_id):
        try:
            actor = Actor.query.get(actor_id)
            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor.id,
            })
        except:
            abort(404)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(token, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie.id,
            })
        except:
            abort(404)

    ## Error Handling

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

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'

        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'

        }), 400

    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        response = jsonify(e.error)
        response.status_code = e.status_code
        return response

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
