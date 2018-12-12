# -*- coding: utf-8 -*-
__author__ = 'gzp'

from collections import namedtuple

Header = namedtuple(
    'Header',
    ('name', 'required', 'value')
)

Param = namedtuple(
    'Param',
    ('name', 'type', 'required', 'desc', 'default', 'value')
)

Response = namedtuple(
    'Response',
    ('header', 'status_code', 'body')
)


type_mapper = {
    str: 'String',
    int: 'Integer'
}
