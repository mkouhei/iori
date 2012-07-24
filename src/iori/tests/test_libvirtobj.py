#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of libvirtobj.py
"""
import unittest
from iori.libvirtobj import Controller


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.l = Controller('localhost')

    def test__init__(self):
        self.assertEqual(self.l.node, 'localhost')
        self.assertTrue(self.l.conn)
