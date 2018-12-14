# -*- coding: utf-8 -*-
__author__ = 'gzp'

from copy import deepcopy
from types import ModuleType

from urllib.parse import urlparse, parse_qs

from rimuru.exceptions import ClientNotSupportError


def doc_client(document, client):
    """

    Decorator for the client that wraps the test request.
    :param document:
    :param client:
    :return:
    """
    __support_clients_decorators = {
        'django.test.client': django_test_client_decorator,
        'requests': requests_decorator
    }

    __support_clients = (
        key for key in __support_clients_decorators.keys()
    )

    name = ''
    if isinstance(client, ModuleType):
        name = client.__name__
    elif isinstance(client, object):
        name = client.__class__.__module__

    if name not in __support_clients:
        raise ClientNotSupportError('Please make sure your client is in %s' % ','.join(__support_clients))

    decorator = __support_clients_decorators[name]
    return decorator(client, document)


def django_test_client_decorator(module, document):
    """
    django.test.client decorator
    :param module:
    :param document:
    :return:
    """
    ori_generic = module.generic

    def wrapped_generic(method, path, data='',
                        content_type='application/octet-stream', secure=False,
                        requires=None, add_response=True, **extra):
        requires = requires if requires else {}
        generator = document.get_generator(method, path)

        parsed_url = urlparse(path)
        extra_copy = deepcopy(extra)

        url_qs = {key: ','.join(value) for key, value in parse_qs(parsed_url.query).items()}
        params = {key: ','.join(value) for key, value in parse_qs(extra_copy.pop('QUERY_STRING', '')).items()}

        api_params = dict(**dict(**(params or {}), **url_qs), **(data or {}))
        for name, value in api_params.items():
            generator.add_params(name, value, requires.get(name))

        headers = {key.replace('HTTP_', '', 1): value for key, value in extra_copy.items()}
        for name, value in (headers or {}).items():
            generator.add_headers(name, value)

        resp = ori_generic(method=method, path=path, data=data, content_type=content_type, secure=secure, **extra)
        resp_headers = dict([each for each in resp._headers.values()])
        converted_body, body_type = generator.convert_response_body(resp.content, resp_headers.get('Content-Type'))
        if add_response:
            generator.add_response(resp.status_code, converted_body, body_type=body_type, headers=resp_headers)

        return resp

    module.generic = wrapped_generic
    return module


def requests_decorator(module, document):
    """
    requests decorator
    :param module:
    :param document:
    :return:
    """
    ori_request = module.Session.request

    def wrapped_request(self, method, url,
                        params=None, data=None, headers=None, cookies=None, files=None,
                        auth=None, timeout=None, allow_redirects=True, proxies=None,
                        hooks=None, stream=None, verify=None, cert=None, json=None, requires=None, add_response=True):
        requires = requires if requires else {}
        generator = document.get_generator(method, url)

        parsed_url = urlparse(url)
        url_qs = {key: ','.join(value) for key, value in parse_qs(parsed_url.query).items()}
        api_params = dict(**dict(**(params or {}), **url_qs), **(data or {}))
        for name, value in api_params.items():
            generator.add_params(name, value, requires.get(name))

        for name, value in (headers or {}).items():
            generator.add_headers(name, value)
        resp = ori_request(self, method=method, url=url,
                           params=params, data=data, headers=headers, cookies=cookies, files=files,
                           auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                           hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

        converted_body, body_type = generator.convert_response_body(resp.content, resp.headers.get('Content-Type'))
        if add_response:
            generator.add_response(resp.status_code, converted_body, body_type=body_type, headers=resp.headers)
        return resp

    module.Session.request = wrapped_request
    return module
