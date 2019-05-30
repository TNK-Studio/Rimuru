# -*- coding: utf-8 -*-
__author__ = 'gzp'

import unittest
import json

from jinja2 import Environment, PackageLoader

from rimuru.utils.jinja2 import filters

from rimuru.core.doc_generator import (
    MarkdownGenerator
)

template_env = Environment(loader=PackageLoader('rimuru', 'templates'))
template_env.cache = None

template_env.filters['success_responses_filter'] = filters.success_responses_filter
template_env.filters['error_responses_filter'] = filters.error_responses_filter
template = 'zh_hans_doc.md'


class MarkdownGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        self.api_name = 'Test API'
        self.api_doc_gen = MarkdownGenerator(
            method='get',
            url='/api/test',
            template=template,
            template_env=template_env,
            name=self.api_name
        )
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
