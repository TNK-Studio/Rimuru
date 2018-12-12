# -*- coding: utf-8 -*-
__author__ = 'gzp'

import unittest
import requests

from rimuru.core import doc_client, APIDocument


class DocClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api_document = APIDocument('.')
        self.client = doc_client(self.api_document, requests)

    def test_doc_client(self):
        response = self.client.get('http://www.baidu.com')
        self.assertEqual(response.status_code, 200)
        self.api_document.set_api_name('get', 'http://www.baidu.com', '百度首页')
        self.api_document.save()
