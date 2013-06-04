# -*- coding: utf-8 -*-

"""
Tests of libvirtobj.py
"""
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import iori.libvirtobj
import iori_tests.test_vars as v


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.l = iori.libvirtobj.Controller('localhost')

    def test__init__(self):
        self.assertEqual(self.l.node, 'localhost')
        self.assertTrue(self.l.conn)

    def test_net_list_of_node(self):
        self.assertDictEqual(v.net_list_of_node,
                             self.l.net_list_of_node())
