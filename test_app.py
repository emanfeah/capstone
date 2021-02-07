import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

Assistant = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im0wbWtWc1dfaFVSaXg5N2tmVldmeCJ9.eyJpc3MiOiJodHRwczovL2RldmU5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDFkOGNiZWYwODMwMzAwNjk1ZWYzZmQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYxMjU0OTM4MywiZXhwIjoxNjEyNTU2NTgzLCJhenAiOiJydTFSa3d6dDl3SkNZdmVjOUFkdkJtYndxbXVTZEZEMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDogYWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.RPm3G33KCUblBegDB0It5Ny5wEsqZ_9v0At4wlF6wxC-8AsCywS3kuF8vhFQGUZ_McFMVwbDZ_NqxugckgFPaxF1_4cXGUXZcx2ZEmXJH9OhAxh__no3u2LMJGEE1XJFL7m_6egubi9_qYbvrJIZCLY3Y_pyouzwUxwT-ewoZXEwIxjD9KMIts9r0JJOmu0L1gMIgdCWOE0Zx6ror_6CDx0wT19J6nO1r8SY92wsAw5C7zkY4PGyrc7Xuv3tQNfduISLwzOyp3RnamznvxHwR0Joh_kSWiB1N11PD_xBgMZMqQbl4yHGbqADUIm4PNOe_O_omhwisPbOGXgw3vtusg'
}

Director = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im0wbWtWc1dfaFVSaXg5N2tmVldmeCJ9.eyJpc3MiOiJodHRwczovL2RldmU5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmZkZWNjZWIxM2U1NzAwNzY4NjcyZGIiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYxMjU0Njc3NSwiZXhwIjoxNjEyNTUzOTc1LCJhenAiOiJydTFSa3d6dDl3SkNZdmVjOUFkdkJtYndxbXVTZEZEMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiLCJyZWFkOiBhY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.YjGsn3eRoFm4mJ5Yo7h2ZuKTzuR0HWhn0ZReUWyTH4NlP4FDQdXUxLVyGg9t-XpvIvP7tKKixR7_BRmupNVFcHnGNIeYSxV7YdZmFjbKsUTaojHiTAavxaGiTCKMk-3ryeCcefUUWH8St_boGcrBcoMBUhHm5keFdfVSDcPagGVTMxHuF9DTBTcqySnSzEPufnoFTzp12nYUrtE0YW9kz1gSxAL29lU0mXuqwzxBDCjtgHQ0ncCG7pc5Z23ySurcb-AADc1RByLkuoWUUBIz0MVj9ARSvfaK90GbUJGg9xDGLGCp-qXw2s8e_PkuaDC7vSvoSO4g78Sha-XiJThXwQ'
}
Executive = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im0wbWtWc1dfaFVSaXg5N2tmVldmeCJ9.eyJpc3MiOiJodHRwczovL2RldmU5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDFjNTg4MTY4NTJhNjAwNmEyMGJkNzAiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYxMjU0Njk2OSwiZXhwIjoxNjEyNTU0MTY5LCJhenAiOiJydTFSa3d6dDl3SkNZdmVjOUFkdkJtYndxbXVTZEZEMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwicmVhZDogYWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.aV5zUxLXrDvCOTkAyuUMASTljlGl3h3gYO_JzJwvij56QI8wiN7wIoFcIc2riw3lHZ6oBb5VlofqE8vwJC8m5FYAwO6ZyXCHUqd9u7ilYty8RPJ0qXdYzMSpelrFS3g_e8Lb-HH7xtVmTZjJn5B48MksMYz29H7XqfsDcmiNXJ9I0reipNUSxMPiWIyL3j8jBWM1ByKxUwlthf1DqMhqD027OkePuW-xFl_PRmWpDCmwnf898uMsiEql2a1sFbbnEbiVvdzqjW5tkFSv3jlBuR3Q912cfY-3uKmLfj-Y6Q-h1yEAxh4ZZIieNxMwmcUr4tN_6fPVDx0qy1HOmnQm0A'

}


class CapstonTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "movie"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'passwad of your postgres', 'localhost:5432',
                                                             self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': "eman",
            'age': "25",
            'gender': "famle"

        }

        self.new_movie = {
            'title': "eman",
            'release_date': "December 19, 2020"

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

    def test_get_actors(self):
        res = self.client().get('/actors', headers=Assistant)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_not_get_actors(self):
        res = self.client().get('/actors')


        self.assertEqual(res.status_code, 401)

    def test_not_get_movies(self):
        res = self.client().get('/movies')

        self.assertEqual(res.status_code, 401)

    def test_create_new_actors(self):
        res = self.client().post('/actors', headers=Director, json={
            'name': "eman",
            'age': "25",
            'gender': "famle"

        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    #
    def test_401_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    #
    def test_create_new_movies(self):
        res = self.client().post('/movies', headers=Director, json={
            'title': "eman",
            'release_date': "December 19, 2020"

        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    #
    def test_401_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    #
    def test_edit_actors(self):
        res = self.client().patch('/actors/2', headers=Director, json={
            'name': "sara",
            'age': "20",
            'gender': "famle"

        })
    #
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #
    def test_not_edit_actors(self):
        res = self.client().patch('/actors/7', json={
            'name': "sara",
            'age': "20",
            'gender': "famle"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
    #
    def test_edit_movies(self):
        res = self.client().patch('/movies/2', headers=Director, json={
            'title': "lolo",
            'release_date': "December 14, 2020"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_not_edit_movies(self):
        res = self.client().patch('/movies/1', json={
            'title': "sara",
            'release_date': "December 14, 2020"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
    #
    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers=Executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    #
    def test_delete_movies(self):
        res = self.client().delete('/movies/1', headers=Executive)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_not_delete_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_not_delete_movies(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
