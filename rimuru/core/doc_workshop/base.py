# -*- coding: utf-8 -*-
__author__ = 'gzp'

from abc import ABC
from typing import Optional, Dict, Tuple
from urllib.parse import urlparse, urlunparse
from werkzeug.routing import Map, Rule, MapAdapter
from werkzeug.exceptions import NotFound

from rimuru.core.doc_generator import (
    APIDocGenerator
)


class APIDocWorkshop(ABC):
    """
    Used to manage document generators
    """
    generator_class: Optional[type(APIDocGenerator)] = None

    def __init__(
            self,
            default_domain: str = 'localhost',
            default_protocol: str = 'http'
    ):
        if not self.generator_class:
            raise NotImplementedError

        self.default_domain: str = default_domain
        self.default_protocol: str = default_protocol
        self.index: APIDocRouteMatcher = APIDocRouteMatcher()
        self.generators: Dict[Tuple[str, str, str], APIDocGenerator] = {}
        self.api_document: Dict[str, Tuple[str, str, str]] = {}

    def __getitem__(self, item):
        generator_key = self.api_document[item]
        return self.generators[generator_key]

    def parse_url(self, url):
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme if parsed_url.scheme else self.default_protocol
        netloc = parsed_url.netloc if parsed_url.netloc else self.default_domain
        path = parsed_url.path
        return scheme, netloc, path

    def set_generator(self, generator_key, method, url_components, name=None):
        self.generators[generator_key] = self.generator_class(
            method, urlunparse(url_components), name=name
        )

    def add_generator(self, method, url, name=None):
        scheme, netloc, path = self.parse_url(url)

        method = method.upper()

        rel_path = self.match_path(netloc, path)

        generator_key = (method, netloc, rel_path)

        url_components = (
            scheme, netloc, rel_path, None, None, None
        )
        self.set_generator(generator_key, method, url_components, name)

    def get_generator(self, method, url):
        _, netloc, path = self.parse_url(url)

        method = method.upper()

        rel_path = self.match_path(netloc, path)

        generator_key = (method, netloc, rel_path)
        doc_generator = self.generators.get(generator_key)
        if not doc_generator:
            self.add_generator(method, url)
            doc_generator = self.generators.get(generator_key)

        return doc_generator

    def set_api_name(self, method, url, name):
        _, netloc, path = self.parse_url(url)

        method = method.upper()
        self.get_generator(method, url).name = name
        self.api_document[name] = (method, netloc, path)

    def save(self, file_path='.'):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

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

