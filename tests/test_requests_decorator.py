# -*- coding: utf-8 -*-
__author__ = 'gzp'

import os
import time
import unittest
import json
import requests as requests_module
from multiprocessing import Process

from rimuru import doc_client, APIDocument
from rimuru.utils.jinja2.filters import (
    success_responses_filter, error_responses_filter
)
from .test_service.flask_ import app

os.environ['NO_PROXY'] = 'localhost'


class RequestsDecoratorTestCase(unittest.TestCase):
    def setUp(self):
        self.api_document = APIDocument()
        requests = doc_client(self.api_document, requests_module)
        self.client = requests

        self.app = app
        self.flask_process = Process(target=self.app.run, args=('localhost', 5000,))
        self.flask_process.start()
        time.sleep(1)  # make sure flask process start

        self.flask_domain = 'localhost:5000'

    def tearDown(self):
        self.flask_process.terminate()
        self.flask_process.join()
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
            url, params={'name': 'A'},
            headers={'TEST_HEADER': 'test'},
            requires={'name': False},
            add_response=False
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
