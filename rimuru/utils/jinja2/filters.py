# -*- coding: utf-8 -*-
__author__ = 'gzp'


def success_responses_filter(responses):
    """
    :param responses:
    :return:
    """
    return [each for each in filter(lambda r: r.status_code == 200, responses)]


def error_responses_filter(responses):
    """
    :param responses:
    :return:
    """
    return [each for each in filter(lambda r: r.status_code >= 400, responses)]
