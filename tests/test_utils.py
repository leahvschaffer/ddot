#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
----------------------------------

Tests for `ddotkit.utils` module.
"""
import io
from contextlib import redirect_stdout
from ddotkit import utils

import unittest


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_print_time(self):
        with redirect_stdout(io.StringIO()) as f:
            utils.print_time('hi')
        res = f.getvalue()
        self.assertTrue(res.startswith('hi '))

    def test_parse_ndex_server(self):
        try:
            utils.parse_ndex_server('http://foo.com')
        except Exception as e:
            self.assertEqual('Not a valid NDEx URL: http://foo.com', str(e))

        self.assertEqual('http://foo.com/',
                         utils.parse_ndex_server('http://foo.com/v2/'
                                                 'network/xxx'))
        self.assertEqual('https://foo.com/',
                         utils.parse_ndex_server('https://foo.com/#/'
                                                 'network/xxx'))

        self.assertEqual('https://ndexbio.org/',
                         utils.parse_ndex_server('https://ndexbio.org/viewer/'
                                                 'networks/xxx'))

    def test_parse_ndex_uuid(self):
        try:
            utils.parse_ndex_uuid('http://foo.com')
        except Exception as e:
            self.assertEqual('Not a valid NDEx URL: http://foo.com', str(e))

        self.assertEqual('',
                         utils.parse_ndex_uuid('http://foo.com/v2/'
                                               'network/'))
        self.assertEqual('',
                         utils.parse_ndex_uuid('http://foo.com/#/'
                                               'network/'))
        self.assertEqual('',
                         utils.parse_ndex_uuid('http://foo.com/viewer/'
                                               'networks/'))
        self.assertEqual('xxx',
                         utils.parse_ndex_uuid('http://foo.com/v2/'
                                               'network/xxx'))
        self.assertEqual('xxx',
                         utils.parse_ndex_uuid('https://foo.com/#/'
                                               'network/xxx'))

        self.assertEqual('xxx',
                         utils.parse_ndex_uuid('https://ndexbio.org/viewer/'
                                               'networks/xxx'))
