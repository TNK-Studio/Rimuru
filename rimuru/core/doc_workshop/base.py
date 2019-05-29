# -*- coding: utf-8 -*-
__author__ = 'gzp'

from typing import Dict
from urllib.parse import urlparse, urlunparse
from werkzeug.routing import Map, Rule, MapAdapter
from werkzeug.exceptions import NotFound

from rimuru.core.doc_generator import APIDocGenerator


class APIDocWorkshop(object):
    """
    Used to manage document generators
    """
    generator_class = APIDocGenerator

    def __init__(self, default_domain='localhost', default_protocol='http'):
        self.default_domain = default_domain
        self.default_protocol = default_protocol
        self.index = APIDocRouteMatcher()
        self.generators = {}
        self.api_document = {}

    def __getitem__(self, item):
        generator_key = self.api_document[item]
        return self.generators[generator_key]

    def parse_url(self, url):
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme if parsed_url.scheme else self.default_protocol
        netloc = parsed_url.netloc if parsed_url.netloc else self.default_domain
        path = parsed_url.path
        return scheme, netloc, path

    def set_generator(self, method, url, name=None):
        scheme, netloc, path = self.parse_url(url)

        method = method.upper()

        rel_path = self.match_path(netloc, path)

        generator_key = (method, netloc, rel_path)

        url_components = (
            scheme, netloc, rel_path, None, None, None
        )

        self.generators[generator_key] = self.generator_class(method, urlunparse(url_components), name=name)

    def get_generator(self, method, url):
        _, netloc, path = self.parse_url(url)

        method = method.upper()

        rel_path = self.match_path(netloc, path)

        generator_key = (method, netloc, rel_path)
        doc_generator = self.generators.get(generator_key)
        if not doc_generator:
            self.set_generator(method, url)
            doc_generator = self.generators.get(generator_key)

        return doc_generator

    def set_api_name(self, method, url, name):
        _, netloc, path = self.parse_url(url)

        method = method.upper()
        self.get_generator(method, url).name = name
        self.api_document[name] = (method, netloc, path)

    def save(self, file_path='.'):
        for doc_generator in self.generators.values():
            if doc_generator.exist_response:
                doc_generator.save(file_path)

    def delete(self):
        for doc_generator in self.generators.values():
            doc_generator.delete()

    def match_path(self, netloc, path):
        rel_path = self.index.match(netloc, path)
        if not rel_path:
            self.index.add(netloc, path)
            rel_path = path
        return rel_path


class APIDocRouteMatcher(object):
    """
    Used to match which route the request address belongs to.
    """
    def __init__(self):
        self.maps: Dict[str, Map] = {}
        self.maps_adapter: Dict[str, MapAdapter] = {}

    def match(self, netloc, path):
        adapter = self.maps_adapter.get(netloc, None)
        if not adapter:
            return None
        try:
            real_path, _ = adapter.match(path)
        except NotFound:
            real_path = None
        return real_path

    def add(self, netloc, path, server_name='localhost'):
        rule_map = self.maps.get(netloc, Map([]))
        rule_map.add(Rule(path, endpoint=path))
        self.maps[netloc] = rule_map
        self.maps_adapter[netloc] = rule_map.bind(server_name)
