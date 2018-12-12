# -*- coding: utf-8 -*-
__author__ = 'gzp'

import unittest
import json

from rimuru.core import APIDocumentGenerator


class APIDocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.api_name = 'Test API'
        self.api_doc = APIDocumentGenerator(self.api_name, method='get', url='/api/test')
        self.api_doc.add_headers('Authorization', 'JWT eyJ0eXAiOiJKV...63XjrurF1bDlv478')
        self.api_doc.add_params('test', 'test')
        self.api_doc.add_response(200, json.dumps({'msg': 'success'}))
        self.api_doc.add_response(400, json.dumps({'msg': 'fail'}))

    def tearDown(self):
        pass

    def test_render(self):
        results = self.api_doc.render()
        print(results)

    def test_save(self):
        self.api_doc.save('.')
