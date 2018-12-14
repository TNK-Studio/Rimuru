# -*- coding: utf-8 -*-
__author__ = 'gzp'

import os
import sys

import django
from django.test import TestCase
from django.test.utils import setup_test_environment

local_path = os.path.split(os.path.realpath(__file__))[0]
django_service_path = os.path.join(local_path, 'test_service/django_')

sys.path.append(local_path)
sys.path.append(django_service_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_.settings'
django.setup()


class DjangoTestClientDecoratorTestCase(TestCase):
    def setUp(self):
        setup_test_environment(debug=True)

    def test_doc_client(self):
        response = self.client.get('/api/books')
        print(response.json())

        success_response = self.client.get('http://127.0.0.1:5000/api/books/2')
        print(success_response.json())

        error_response = self.client.get('http://127.0.0.1:5000/api/books/4')
        print(error_response.json())
