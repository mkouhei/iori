# -*- coding: utf-8 -*-

"""
Tests of control.py
"""
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import iori.control


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.dirpath = '/tmp/iori_test'
        self.node = 'localhost'
        self.ctl = iori.control.Control(self.dirpath)
        self.ctl2 = iori.control.Control(self.dirpath, self.node)

    def test__init__(self):
        self.assertTrue(self.ctl.r)
        self.assertTrue(self.ctl.c)
        self.assertTrue(self.ctl.dirpath, self.dirpath)

        self.assertTrue(self.ctl2.r)
        self.assertTrue(self.ctl2.c)
        self.assertTrue(self.ctl2.l)
        self.assertTrue(self.ctl2.dirpath, self.dirpath)
