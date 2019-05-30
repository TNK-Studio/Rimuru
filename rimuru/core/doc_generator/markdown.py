# -*- coding: utf-8 -*-
__author__ = 'gzp'

import os
import inspect
import re
from typing import Optional

from jinja2 import Environment, PackageLoader

from rimuru.utils.jinja2 import filters

from .base import APIDocGenerator

env = Environment(loader=PackageLoader('rimuru', 'templates'))
env.cache = None

env.filters['success_responses_filter'] = filters.success_responses_filter
env.filters['error_responses_filter'] = filters.error_responses_filter


class MarkdownGenerator(APIDocGenerator):
    def __init__(
            self,
            method,
            url,
            template,
            template_env,
            name='',
            **kwargs
    ):
        self.template = template
        self.template_env = template_env

        super().__init__(method, url, name=name, **kwargs)

    @classmethod
    def pre_process(cls, content):
        content = re.sub(r'\n{2,}', '\n\n', content)
        return content

    def render(self):
        template = self.template_env.get_template(self.template)
        return template.render(**{attr: value for attr, value in inspect.getmembers(self)})

    def save(self, output):
        file_suffix = self.template.split('.')[-1] if '.' in self.template else ''
        path = os.path.join(output, '%s.%s' % (self.name, file_suffix))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.pre_process(self.render()))
            self.file_path = path
