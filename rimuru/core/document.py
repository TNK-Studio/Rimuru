# -*- coding: utf-8 -*-
__author__ = 'gzp'

from rimuru.core.generator import APIDocumentGenerator


class APIDocument(object):
    generator_class = APIDocumentGenerator

    def __init__(self, path):
        self.generators = {}
        self.path = path if path else '.'

    def set_generator(self, method, url, name=None):
        self.generators[(method, url)] = self.generator_class(method.upper(), url, name=name)

    def get_generator(self, method, url):
        generator = self.generators.get((method.upper(), url))
        if not generator:
            self.set_generator(method.upper(), url)
            generator = self.generators.get((method.upper(), url))

        return generator

    def set_api_name(self, method, url, name):
        self.get_generator(method.upper(), url).name = name

    def save(self):
        for generator in self.generators.values():
            if generator.exist_response:
                generator.save(self.path)

