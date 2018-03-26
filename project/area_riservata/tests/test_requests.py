#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json

from django.test import TestCase
from rest_framework.test import RequestsClient


class RequestTest(TestCase):

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
        self.client_stub = RequestsClient()


    def test_create_seduta(self):
        with open('./resources/fixtures/seduta.json', 'r') as f:
            seduta = json.load(f)

        r = self.client_stub.post(
            'http://localhost:8000/api-token-auth/',
            data={"username": "mosic", "password": "mosicmosic"}
        ).json()


        response = self.client_stub.post(
            'http://localhost:8000/precipe',
            json=seduta,
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 201)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/files/Architettura 1 blocco.pdf',
            files={'file': open('./resources/fixtures/docs/architettura.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/files/JWTHandbook.pdf',
            files={'file': open('./resources/fixtures/docs/jwt_handbook.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/frugs/JWTHandbook.pdf',
            files={'file': open('./resources/fixtures/docs/jwt_handbook.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

        response = self.client_stub.get(
            'http://localhost:8000/precipe/1',
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 200)

        response = self.client_stub.delete(
            'http://localhost:8000/precipe/1',
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

    def test_create_seduta_with_duplicates(self):
        with open('./resources/fixtures/duplicates_1.json', 'r') as f:
            seduta_1 = json.load(f)

        with open('./resources/fixtures/duplicates_2.json', 'r') as f:
            seduta_2 = json.load(f)

        r = self.client_stub.post(
            'http://localhost:8000/api-token-auth/',
            data={"username": "mosic", "password": "mosicmosic"}
        ).json()

        response = self.client_stub.post(
            'http://localhost:8000/precipe',
            json=seduta_1,
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 201)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/files/torino.pdf',
            files={'file': open('./resources/fixtures/docs/torino.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

        response = self.client_stub.post(
            'http://localhost:8000/precipe',
            json=seduta_2,
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 201)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/files/torino.pdf',
            files={'file': open('./resources/fixtures/docs/torino.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

    def test_create_seduta_long_names(self):
        with open('./resources/fixtures/seduta_long_names.json', 'r') as f:
            seduta = json.load(f)

        r = self.client_stub.post(
            'http://localhost:8000/api-token-auth/',
            data={"username": "mosic", "password": "mosicmosic"}
        ).json()


        response = self.client_stub.post(
            'http://localhost:8000/precipe',
            json=seduta,
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 201)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/files/Architettura 1 blocco.pdf',
            files={'file': open('./resources/fixtures/docs/architettura.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/files/7185-All-4-Piano-annuale-degli-interventi-di-ricostruzione-del-patrimonio-pubblico-della-citta-di-LAquila-e-dei-comuni-del-Cratere.pdf',
            files={'file': open('./resources/fixtures/docs/jwt_handbook.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

        response = self.client_stub.get(
            'http://localhost:8000/precipe/1',
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 200)

        response = self.client_stub.delete(
            'http://localhost:8000/precipe/1',
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)


    def test_create_seduta_big_files(self):
        with open('./resources/fixtures/seduta_big_files.json', 'r') as f:
            seduta = json.load(f)

        r = self.client_stub.post(
            'http://localhost:8000/api-token-auth/',
            data={"username": "mosic", "password": "mosicmosic"}
        ).json()


        response = self.client_stub.post(
            'http://localhost:8000/precipe',
            json=seduta,
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 201)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/files/Architettura 1 blocco.pdf',
            files={'file': open('./resources/fixtures/docs/architettura.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

        response = self.client_stub.put(
            'http://localhost:8000/upload_file/files/D3JS_4_MAPPING_SECOND_EDITION.pdf',
            files={'file': open('./resources/fixtures/docs/D3JS_4_MAPPING_SECOND_EDITION.pdf', 'rb')},
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)

        response = self.client_stub.get(
            'http://localhost:8000/precipe/1',
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 200)

        response = self.client_stub.delete(
            'http://localhost:8000/precipe/1',
            headers={'Authorization': 'JWT ' + r['token']}
        )
        self.assertEquals(response.status_code, 204)
