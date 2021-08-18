#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
----------------------------------

Tests for `ddotkit.config` module.
"""

from ddotkit import config

import unittest


class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getpassthrough_style(self):
        net = config.get_passthrough_style()
        self.assertIsNotNone(net, 'checking we did not get None for style file')
        self.assertEqual(8, len(net.get_nodes()),
                         'Checking that number of nodes '
                         'matches expected value in style')
