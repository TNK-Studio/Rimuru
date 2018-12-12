# -*- coding: utf-8 -*-
__author__ = 'gzp'

import os
import inspect
from jinja2 import Environment, PackageLoader

from rimuru.definitions import (
    Header, Param, Response, type_mapper
)
from rimuru.utils.jinja2 import filters

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

    def __init__(self, name, method, url, note=''):
        self.name = name
        self.method = method.upper()
        self.url = url

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

    def add_response(self, status_code, body, header=''):
        self.responses.add(
            self.response_class(
                status_code=status_code, body=body, header=header
            )
        )
