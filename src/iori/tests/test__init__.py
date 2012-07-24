#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of __init__.py
"""
import unittest
import iori


class InitTests(unittest.TestCase):
    def test_version_defined(self):
        actual_version = iori.__version__
        self.assertTrue(actual_version)

if __name__ == '__main__':
    unittest.main()
