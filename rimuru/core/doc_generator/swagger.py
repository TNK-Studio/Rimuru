# -*- coding: utf-8 -*-
__author__ = 'gzp'

from typing import Optional, List
from .base import APIDocGenerator
from urllib.parse import urlparse, urlunparse


class SwaggerGenerator(APIDocGenerator):

    def __int__(
            self,
            *args,
            description: str = '',
            version: str = '1.0.0',
            schemes: Optional[List[str]] = None,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title = self.name
        self.description = description
        self.version = version
        self.schemes = schemes
        if self.schemes:
            self.schemes = []

        parsed_url = urlparse(self.url)
        self.host = parsed_url.netloc
        self.schemes.append(parsed_url.scheme)

    def save(self, output):
        pass
