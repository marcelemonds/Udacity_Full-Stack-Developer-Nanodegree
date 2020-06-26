import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors, db

tokens = {
    'casting_assistent': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56Z3pSRUpETkRrMU56QTNSVEpET1VWQk5UTkRRemd6TlRSR09USkZPVGhDT0RBMU1URkJSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMzQxbDk3aS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlYTRjY2NjYTZmNDgwMDE5OTgzYTNjIiwiYXVkIjpbImNhcHN0b25lIiwiaHR0cHM6Ly9kZXYtYTM0MWw5N2kuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MjU1NDQ0MSwiZXhwIjoxNTk1MTQ2NDQxLCJhenAiOiJsVlMzVElvQ1NYVGFhWnM5RHlVM1kwNGtZQ1h4dzROViIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.g2S3Evi83CUB1r27N3EG5ujF4POgRMLZj1xsyfAzDPXqsA5xgcckkaHaHAebKC5E3ZXzYniww_NcJdZgUAFO7K_tGl5Gmxhtp1j34QWVhNj-o0xvB9ikXrPd0fOlKt7J76uxk5d8a1OK5dEPqI09XiiSPuJeOYNGsqcRNnVEVeXFka2ofgfAQZLCKPHF6dEkXOl1Mtu7e72zUIKvpjQrdjVELghwdYu8U24wCXrluSKJyYKM39NedXPaNWdC130MxIpC3v4vxiAdHyIHif-UM7LyY1CB9ibH79j7MGMdMk7OqaKFxWqMrp2ygJ1ZostIyjdpsv60zUoBlI0s26K1vw',
    'casting_director': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56Z3pSRUpETkRrMU56QTNSVEpET1VWQk5UTkRRemd6TlRSR09USkZPVGhDT0RBMU1URkJSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMzQxbDk3aS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlYTdiMzliOWI1OTEwMDEzY2JjMDQyIiwiYXVkIjpbImNhcHN0b25lIiwiaHR0cHM6Ly9kZXYtYTM0MWw5N2kuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MjU1NDQwMSwiZXhwIjoxNTk1MTQ2NDAxLCJhenAiOiJsVlMzVElvQ1NYVGFhWnM5RHlVM1kwNGtZQ1h4dzROViIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.fXIxYNsly-3su3gxuuRdpjL0NIK0a7oZnnPz_LdK5Z5kldTieDlwY0KugZ2vqqwzLq-NicKkkgZKMsh485A4tEGybBzISm38FXZup7xZSrSwsHZdpKOwq8VHaprIT-Z9Z5BV9PRdPhdTaaIw2w3KfTup6g6Iw8PKHfBzzOdHtN99fBjAB0sB62_1Yz0nLqL222kpG7-mgmHl1lJla90PuF_O2QqjyPrfjFvKM-uGJqkeGhbrXFRamCFF8lOYCWwnU_9qZaNCrrgcRV6-MW81Y8PJXMXTx3x_X0i5CHx187K4-GWE6WRPcFxq6DNaDlDIw-bsA6zgVTot0yOFJ9kCkw',
    'executive_producer': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56Z3pSRUpETkRrMU56QTNSVEpET1VWQk5UTkRRemd6TlRSR09USkZPVGhDT0RBMU1URkJSUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1hMzQxbDk3aS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlYTdiN2NiOGE2NTkwMDE5ZTViYTk4IiwiYXVkIjpbImNhcHN0b25lIiwiaHR0cHM6Ly9kZXYtYTM0MWw5N2kuZXUuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MjU1NDQ3OSwiZXhwIjoxNTk1MTQ2NDc5LCJhenAiOiJsVlMzVElvQ1NYVGFhWnM5RHlVM1kwNGtZQ1h4dzROViIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.BE0AmO56SYtoB3m-Y29mVWKWd2kGg5ossS4l_vDb1dX-UFFyrbG0CjpRG9YONTKv-W4jFM4AUjJO1GksQcQawlcRRmOXRqbdF6mx2uYPEH7KTb80bNdOHlQx7S45u4l5g-0jq0Dw_qig-ZwCgqFCM3BtYd0NZA5L5kUWxggq5e80ckrqPK52GvxruEYsg7-KywWqZcsGLTNLYAAnuiEv7peRrSHDWBj5GlXgHWdAmm0qkbX27sJQCVmK5N1cgFJWArAyvG_tKslHy2COVzRPQ1MiNdv66pEywbhHBd9lupLaFCXhWTGss8Kt5RXhK0-7zzclDV9OGfMvTORhntLrZw'
}

header_casting_assistent = {
    'Authorization': tokens['casting_assistent']
}

header_casting_director = {
    'Authorization': tokens['casting_director']
}

header_executive_producer = {
    'Authorization': tokens['executive_producer']
}


class ApiTestCase(unittest.TestCase):

    def insert_data(self):
        dummy_movie_1 = Actors(
            name='dummy_movie_1',
            age=36,
            gender='m'
            )
        dummy_actor_2 = Actors(
            name='dummy_actor_2',
            age=35,
            gender='f'
            )
        dummy_actor_3 = Actors(
            name='dummy_actor_3',
            age=34,
            gender='m'
            )
        self.db.session.add(dummy_movie_1)
        self.db.session.add(dummy_actor_2)
        self.db.session.add(dummy_actor_3)

        dummy_movie_1 = Movies(
            title='dummy_movie_1',
            release_date='2019-12-12'
            )
        dummy_movie_2 = Movies(
            title='dummy_movie_2',
            release_date='2019-12-13'
            )
        dummy_movie_3 = Movies(
            title='dummy_movie_3',
            release_date='2019-12-14'
            )
        self.db.session.add(dummy_movie_1)
        self.db.session.add(dummy_movie_2)
        self.db.session.add(dummy_movie_3)

        self.db.session.commit()
        self.db.session.close()

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        db_sql_dialect = 'postgres'
        db_username = 'postgres'
        db_password = '1234'
        db_host = 'localhost'
        db_database = 'capstone'

        database_path = f'{db_sql_dialect}://{db_username}:{db_password}@{db_host}/{db_database}'
        setup_db(self.app, database_path=database_path)
        with self.app.app_context():
            self.db = db
            self.db.drop_all()
            self.db.create_all()
            self.insert_data()

    def tearDown(self):
        self.db.session.rollback()
        self.db.drop_all()
        self.db.session.close()
        pass

    # --------------------------------
    # tests for GET actors
    #   success: get actors with correct permissions
    #   failure: get actors without permissions
    # --------------------------------
    def test_success_get_actors(self):
        response = self.client().get('/api/actors',
                                     headers=header_casting_assistent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_failure_get_actors(self):
        response = self.client().get('/api/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # --------------------------------
    # tests for POST actors
    #   success: post new actor
    #   failure: post new actor with incomplete json body
    # --------------------------------
    def test_success_post_actors(self):
        post_actor = {
            'name': 'Actor1',
            'gender': 'male',
            'age': 36
        }
        response = self.client().post('/api/actors',
                                      json=post_actor,
                                      headers=header_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_failure_post_actors(self):
        new_actor = {
            'name': 'Actor1',
            'gender': 'male'
        }
        response = self.client().post('/api/actors',
                                      json=new_actor,
                                      headers=header_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable')

    # --------------------------------
    # tests for PATCH actors
    #   success: patch existing actor
    #   failure: patch without json body
    # --------------------------------
    def test_success_patch_actors(self):
        patch_actor = {
            'name': 'new_name'
        }
        response = self.client().patch('/api/actors/1',
                                       json=patch_actor,
                                       headers=header_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_failure_patch_actors(self):
        response = self.client().patch('/api/actors/1',
                                       headers=header_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    # --------------------------------
    # tests for DELETE actors
    #   success: delete existing actor
    #   failure: delete existing actor with incorrect permissions
    # --------------------------------
    def test_success_delete_actors(self):
        response = self.client().delete('/api/actors/1',
                                        headers=header_executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_failure_delete_actors(self):
        response = self.client().delete('/api/actors/1',
                                        headers=header_casting_assistent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    # --------------------------------
    # tests for GET movies
    #   success: get actors with correct permissions
    #   failure: get actors without permissions
    # --------------------------------
    def test_success_get_movies(self):
        response = self.client().get('/api/movies',
                                     headers=header_casting_assistent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_failure_get_movies(self):
        response = self.client().get('/api/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # --------------------------------
    # tests for POST movies
    #   success: post new movie
    #   failure: post new movie with incomplete json body
    # --------------------------------
    def test_success_post_movies(self):
        new_movie = {
            'title': 'test_movie',
            'release_date': "2019-12-24"
        }
        response = self.client().post('/api/movies',
                                      json=new_movie,
                                      headers=header_executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_failure_post_movies(self):
        new_actor = {
            'title': 'test_movie'
        }
        response = self.client().post('/api/movies',
                                      json=new_actor,
                                      headers=header_executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable')

    # --------------------------------
    # tests for PATCH movies
    #   success: patch existing movie
    #   failure: patch without json body
    # --------------------------------
    def test_success_patch_movies(self):
        patch_movie = {
            "title": "test_movie"
        }
        response = self.client().patch('/api/movies/1',
                                       json=patch_movie,
                                       headers=header_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_failure_patch_movies(self):
        response = self.client().patch('/api/movies/1',
                                       headers=header_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    # --------------------------------
    # tests for DELETE movies
    #   success: delete existing movie
    #   failure: delete existing movie with incorrect permissions
    # --------------------------------
    def test_success_delete_movies(self):
        response = self.client().delete('/api/movies/1',
                                        headers=header_executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_failure_delete_movies(self):
        response = self.client().delete('/api/movies/1',
                                        headers=header_casting_assistent)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')


if __name__ == "__main__":
    unittest.main()
