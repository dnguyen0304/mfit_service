# -*- coding: utf-8 -*-

import abc

import requests
from nose.tools import assert_equal, assert_true


class Base(metaclass=abc.ABCMeta):

    api_version = 'v1'
    root_url = 'http://127.0.0.1:5000/' + api_version + '/'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    @property
    @abc.abstractmethod
    def endpoint_name(self):
        return ''

    @property
    def url(self):
        url = self.root_url
        if self.endpoint_name.lower().strip() != 'root':
            url += self.endpoint_name
        if not url.endswith('/'):
            url += '/'
        return url

    def test_get_status_code(self):
        response = requests.head(url=self.url, headers=self.headers)
        assert_true(response.ok)

    def test_self_link(self):
        response = requests.get(url=self.url, headers=self.headers)
        assert_equal(self.url, response.json()['links']['self'])

    def test_is_discoverable(self):
        response = requests.get(url=self.root_url, headers=self.headers)
        discovered_url = response.json()['data'].get(self.endpoint_name, '')
        assert_equal(discovered_url, self.url)

