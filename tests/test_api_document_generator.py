# -*- coding: utf-8 -*-
__author__ = 'gzp'

import unittest
import json

from rimuru.core import APIDocumentGenerator


class APIDocumentGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.api_name = 'Test API'
        self.api_doc_gen = APIDocumentGenerator(method='get', url='/api/test', name=self.api_name)
        self.api_doc_gen.add_headers('Authorization', 'JWT eyJ0eXAiOiJKV...63XjrurF1bDlv478')
        self.api_doc_gen.add_params('test', 'test')
        self.api_doc_gen.add_response(200, json.dumps({'msg': 'success'}), body_type='json')
        self.api_doc_gen.add_response(400, json.dumps({'msg': 'fail'}), body_type='json')

    def tearDown(self):
        self.api_doc_gen.delete()

    def test_render(self):
        results = self.api_doc_gen.render()
        print(results)

    def test_save(self):
        self.api_doc_gen.save('.')
        self.assertEqual(self.api_doc_gen.saved, True)
