# -*- coding: utf-8 -*-
__author__ = 'gzp'

import os
import inspect
import json

from jinja2 import Environment, PackageLoader

from rimuru.definitions import (
    Header, Param, Response, type_mapper
)
from rimuru.utils.jinja2 import filters

env = Environment(loader=PackageLoader('rimuru', 'templates'))
env.cache = None

env.filters['success_responses_filter'] = filters.success_responses_filter
env.filters['error_responses_filter'] = filters.error_responses_filter


def decode_utf8(bytes):
    return bytes.decode('utf-8')


class APIDocumentGenerator(object):
    template = 'zh_hans_doc.md'
    env = env

    header_class = Header
    param_class = Param
    response_class = Response

    type_mapper = type_mapper
    response_body_handlers = (
        ('text/html', decode_utf8, 'html'),
        ('application/json', json.dumps, 'json'),
    )

    def __init__(self, method, url, name='', note=''):
        self.name = name if name else '%s %s' % (method, url)
        self.method = method.upper()
        self.url = url

        self.response_body_handlers_map = {
            content_type: (handler, body_type)
            for content_type, handler, body_type in self.response_body_handlers
        }

        self.note = note

        self.headers = set()
        self.params = set()
        self.responses = set()

    def render(self):
        template = env.get_template(self.template)
        return template.render(**{attr: value for attr, value in inspect.getmembers(self)})

    def save(self, output, file_suffix='md'):
        with open(os.path.join(output, '%s.%s' % (self.name, file_suffix)), 'w', encoding='utf-8') as f:
            f.write(self.render())

    def add_headers(self, name, value, required=True, *kwargs):
        self.headers.add(
            self.header_class(
                name=name, value=value, required=required, *kwargs
            )
        )

    def add_params(self, name, value, required=True, desc='', param_type=None, default=''):
        param_type = param_type if param_type else self.type_mapper.get(type(value), 'String')
        self.params.add(
            self.param_class(
                name=name, value=value, required=required, desc=desc, type=param_type, default=default
            )
        )

    def add_response(self, status_code, body, headers=None, body_type=None):
        headers = headers if headers else {}
        headers = '\n'.join(['%s: %s' % (key, value) for key, value in headers.items()])
        body_type = body_type if body_type else ''
        self.responses.add(
            self.response_class(
                status_code=status_code, body=body, headers=headers, type=body_type
            )
        )

    def convert_response_body(self, body, content_type):
        result = self.response_body_handlers_map.get(content_type)
        body_type = None
        if result:
            handler, body_type = result
            body = handler(body)

        return body, body_type

    @property
    def exist_response(self):
        return len(self.responses) > 0
