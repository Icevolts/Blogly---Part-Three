from unittest import TestCase
from models import User
from app import app

class PageTestCase(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_create_user(self):
        with self.client:
            res = self.client.post('/users/new', data = {'first_name': 'Gerald', 'last_name': 'Walters', 'image_url': 'None'})
        self.assertEqual(res.status_code,302)
        self.assertEqual(res.location,'/users')
    
    def test_delete_user(self):
        with self.client:
            user_id = 9999
            res = self.client.post(f'/users/{user_id}/delete')
        self.assertEqual(res.status_code,404)

    def test_create_post(self):
        with self.client:
            res = self.client.post('/users/1/posts/new', data = {'title': 'Hello', 'content': 'Hello World'})
        self.assertEqual(res.status_code,302)
        self.assertEqual(res.location,'/users/1')

    def test_delete_post(self):
        with self.client:
            post_id = 9999
            res = self.client.post(f'/posts/{post_id}/delete')
        self.assertEqual(res.status_code,404)

    def test_create_tag(self):
        with self.client:
            res = self.client.post('/tags/new', data = {'name': 'fun'})
        self.assertEqual(res.status_code,302)
        self.assertEqual(res.location,'/tags')

    def test_delete_post(self):
        with self.client:
            tag_id = 9999
            res = self.client.post(f'/tags/{tag_id}/delete')
        self.assertEqual(res.status_code,404)   