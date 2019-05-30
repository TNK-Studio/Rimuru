# -*- coding: utf-8 -*-
__author__ = 'gzp'

from typing import Optional
from jinja2 import Environment, PackageLoader
from urllib.parse import urlunparse

from rimuru.utils.jinja2 import filters

from rimuru.core.doc_generator import (
    MarkdownGenerator
)

from .base import APIDocWorkshop

template_env = Environment(loader=PackageLoader('rimuru', 'templates'))
template_env.cache = None

template_env.filters['success_responses_filter'] = filters.success_responses_filter
template_env.filters['error_responses_filter'] = filters.error_responses_filter


class MarkdownWorkShop(APIDocWorkshop):
    generator_class = MarkdownGenerator
    template = 'zh_hans_doc.md'
    template_env = template_env

    def __init__(self, *args, template: Optional[str] = None, template_env: Optional[Environment] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if template:
            self.template = template

        if template_env:
            self.template_env = template_env

    def set_generator(self, generator_key, method, url_components, name=None):
        self.generators[generator_key] = self.generator_class(
            method,
            urlunparse(url_components),
            self.template,
            self.template_env,
            name=name
        )

    def save(self, file_path='.'):
        for doc_generator in self.generators.values():
            if doc_generator.exist_response:
                doc_generator.save(file_path)

    def delete(self):
        for doc_generator in self.generators.values():
            doc_generator.delete()
