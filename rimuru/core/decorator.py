# -*- coding: utf-8 -*-
__author__ = 'gzp'

from rimuru.exceptions import ClientNotSupportError


def doc_client(document, client):
    __support_clients_decorators = {
        'django.test.client': django_test_client_decorator,
        'requests': requests_decorator
    }

    __support_clients = (
        key for key in __support_clients_decorators.keys()
    )

    if client.__name__ not in __support_clients:
        raise ClientNotSupportError('Please make sure your client is in %s' % ','.join(__support_clients))

    decorator = __support_clients_decorators[client.__name__]
    return decorator(client, document)


def django_test_client_decorator(module, document):
    return module


def requests_decorator(module, document):
    ori_request = module.Session.request

    def wrapped_request(self, method, url,
                        params=None, data=None, headers=None, cookies=None, files=None,
                        auth=None, timeout=None, allow_redirects=True, proxies=None,
                        hooks=None, stream=None, verify=None, cert=None, json=None, requires=None):
        requires = requires if requires else {}
        generator = document.get_generator(method, url)
        api_params = dict(**(params or {}), **(data or {}))
        for name, value in api_params.items():
            generator.add_params(name, value, requires.get(name))

        for name, value in (headers or {}).items():
            generator.add_headers(name, value)
        resp = ori_request(self, method=method, url=url,
                           params=params, data=data, headers=headers, cookies=cookies, files=files,
                           auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies,
                           hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

        converted_body, body_type = generator.convert_response_body(resp.content, resp.headers.get('Content-Type'))
        generator.add_response(resp.status_code, converted_body, body_type=body_type, headers=resp.headers)
        return resp

    module.Session.request = wrapped_request
    return module
