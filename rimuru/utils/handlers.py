# -*- coding: utf-8 -*-
__author__ = 'gzp'

import json


def decode_utf8(body):
    return body.decode('utf-8')


def pretty_json(data):
    parsed = json.loads(data)
    return json.dumps(parsed, indent=4, sort_keys=True)


def json_body_handler(body):
    return pretty_json(body.decode('utf-8'))
