#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests of control.py
"""
import unittest
from iori.control import Control


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.dirpath = '/tmp/iori_test'
        self.node = 'localhost'
        self.ctl = Control(self.dirpath)
        self.ctl2 = Control(self.dirpath, self.node)

    def test__init__(self):
        self.assertTrue(self.ctl.r)
        self.assertTrue(self.ctl.c)
        self.assertTrue(self.ctl.dirpath, self.dirpath)

        self.assertTrue(self.ctl2.r)
        self.assertTrue(self.ctl2.c)
        self.assertTrue(self.ctl2.l)
        self.assertTrue(self.ctl2.dirpath, self.dirpath)
