# -*- coding: utf-8 -*-
__author__ = 'gzp'

import os
import inspect
import re

from jinja2 import Environment, PackageLoader

from rimuru.definitions import (
    Header, Param, Response, type_mapper
)
from rimuru.utils.jinja2 import filters
from rimuru.utils.handlers import (
    decode_utf8, json_body_handler
)

env = Environment(loader=PackageLoader('rimuru', 'templates'))
env.cache = None

env.filters['success_responses_filter'] = filters.success_responses_filter
env.filters['error_responses_filter'] = filters.error_responses_filter


class APIDocumentGenerator(object):
    template = 'zh_hans_doc.md'
    env = env

    header_class = Header
    param_class = Param
    response_class = Response

    type_mapper = type_mapper
    response_body_handlers = (
        ('text/html', decode_utf8, 'html'),
        ('application/json', json_body_handler, 'json'),
    )

    def __init__(self, method, url, name='', **kwargs):
        self.name = name if name else '%s %s' % (method, url)
        self.method = method.upper()
        self.url = url

        self.response_body_handlers_map = {
            content_type: (handler, body_type)
            for content_type, handler, body_type in self.response_body_handlers
        }
        self._headers = dict()
        self._params = dict()
        self._responses = set()

        self.file_path = None

        for key, value in kwargs:
            self.set_value(key, value)

    @property
    def headers(self):
        return [value for value in self._headers.values()]

    @property
    def params(self):
        return [value for value in self._params.values()]

    @property
    def responses(self):
        return list(self._responses)

    def set_value(self, key, value):
        setattr(self, key, value)

    def render(self):
        template = env.get_template(self.template)
        return template.render(**{attr: value for attr, value in inspect.getmembers(self)})

    @classmethod
    def pre_process(cls, content):
        content = re.sub(r'\n{2,}', '\n\n', content)
        return content

    def save(self, output):
        file_suffix = self.template.split('.')[-1] if '.' in self.template else ''
        path = os.path.join(output, '%s.%s' % (self.name, file_suffix))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.pre_process(self.render()))
            self.file_path = path

    def delete(self):
        if self.saved:
            os.remove(self.file_path)

    @property
    def saved(self):
        return self.file_path and os.path.exists(self.file_path)

    def add_headers(self, name, value, required=True, *kwargs):
        self._headers[name] = self.header_class(
            name=name, value=value, required=required, *kwargs
        )

    def add_params(self, name, value, required=True, desc='', param_type=None, default=''):
        param_type = param_type if param_type else self.type_mapper.get(type(value), 'String')

        self._params[name] = self.param_class(
            name=name, value=value, required=required, desc=desc, type=param_type, default=default
        )

    def add_response(self, status_code, body, headers=None, body_type=None):
        headers = headers if headers else {}
        headers = '\n'.join(['%s: %s' % (key, value) for key, value in headers.items()])
        body_type = body_type if body_type else ''
        self._responses.add(
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
