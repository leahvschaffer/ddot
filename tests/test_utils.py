#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
----------------------------------

Tests for `ddotkit.utils` module.
"""

from ddotkit import utils

import unittest


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_print_time(self):
        utils.print_time('hi')
