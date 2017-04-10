import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class ViewTest(TestCase):

    def setUp(self):
        """
        create client_stub and load users and groups from fixtures
        contenttypes, sites, and permissions are already in test db
        
        so, in order to create users and group, it is sufficient to invoke:
        python project/manage.py dumpdata --natural-foreign \
          --exclude=auth.permission auth \
          --indent=4 > resources/fixtures/setup.json
        
        :return:
        """
        from django.core.management import call_command
        call_command("loaddata", "setup", verbosity=0)
        self.client_stub = APIClient()


    def test_view_home_forbidden_to_anon_users(self):
        response = self.client_stub.get('/')
        self.assertEquals(response.status_code, 401)

    def test_obtain_jwt_token(self):
        response = self.client_stub.post(
            '/api-token-auth/',
            {"username": "mosic", "password": "mosicmosic"})
        self.assertEquals(response.status_code, 200)
        r = response.json()
        self.assertIn('token', r.keys(), "token not in response")

    def test_view_home_accessible_with_token(self):
        r = self.client_stub.post(
            '/api-token-auth/',
            {"username": "mosic", "password": "mosicmosic"}
        ).json()
        token = r['token']
        self.client_stub.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client_stub.get('/')
        self.assertEquals(response.status_code, 200)

    def test_create_seduta_from_json(self):
        with open('./resources/fixtures/seduta.json', 'r') as f:
            seduta = json.load(f)

        r = self.client_stub.post(
            '/api-token-auth/',
            {"username": "mosic", "password": "mosicmosic"}
        ).json()
        self.client_stub.credentials(HTTP_AUTHORIZATION='JWT ' + r['token'])
        response = self.client_stub.post(
            '/seduta/', seduta
        )
        self.assertEquals(response.status_code, 201)

        response = self.client_stub.get('/seduta/1/')
        print(json.dumps(response.json(), indent=4))
        self.assertEquals(response.status_code, 200)
