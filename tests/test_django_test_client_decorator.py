# -*- coding: utf-8 -*-
__author__ = 'gzp'

import os
import sys
import json
import django
from django.test import TestCase
from django.test.utils import setup_test_environment

from rimuru import doc_client, APIDocument
from rimuru.utils.jinja2.filters import (
    success_responses_filter, error_responses_filter
)

local_path = os.path.split(os.path.realpath(__file__))[0]
django_service_path = os.path.join(local_path, 'test_service/django_')

sys.path.append(local_path)
sys.path.append(django_service_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_.settings'
django.setup()


class DjangoTestClientDecoratorTestCase(TestCase):
    def setUp(self):
        setup_test_environment(debug=True)
        self.api_document = APIDocument()
        self.client = doc_client(self.api_document, self.client)

    def tearDown(self):
        self.api_document.delete()

    def test_doc_client(self):
        url = 'http://127.0.0.1:5000/api/books'
        method = 'GET'
        name = '书列表接口'
        self.api_document.set_api_name(method=method, url=url, name=name)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        generator = self.api_document['书列表接口']

        self.assertEqual(generator.method, method)
        self.assertEqual(generator.url, url)
        generator_response = generator.responses[0]
        self.assertEqual(generator_response.status_code, response.status_code)
        self.assertEqual(response.json(), json.loads(generator_response.body))

        self.client.get(
            url, data={'name': 'A'},
            requires={'name': False},
            add_response=False,
            **{'HTTP_TEST_HEADER': 'test'}
        )
        self.assertGreater(len(generator.params), 0)
        generator_params = generator.params[0]

        # 确定参数都在文档中
        self.assertEqual(generator_params.name, 'name')
        self.assertEqual(generator_params.type, 'String')
        self.assertEqual(generator_params.required, False)
        self.assertEqual(generator_params.value, 'A')

        url = 'http://127.0.0.1:5000/api/books/<int:id>'
        method = 'GET'
        name = '书详情接口'
        self.api_document.set_api_name(method=method, url=url, name=name)
        generator = self.api_document[name]

        success_response = self.client.get('http://127.0.0.1:5000/api/books/2')
        error_response = self.client.get('http://127.0.0.1:5000/api/books/4')

        # 验证错误和正确返回值都在文档中
        self.assertEqual(json.loads(success_responses_filter(generator.responses)[0].body), success_response.json())
        self.assertEqual(json.loads(error_responses_filter(generator.responses)[0].body), error_response.json())

        self.api_document.save(file_path='tests/')
        for each_generator in self.api_document.generators.values():
            self.assertEqual(each_generator.saved, True)
            with open(each_generator.file_path, 'r', encoding='utf-8') as f:
                print(f.read())
