# -*- coding: utf-8 -*-

"""
Tests of repo.py
"""
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import iori.repo


class RepoTests(unittest.TestCase):
    def setUp(self):
        self.dirpath = '/tmp/iori_test'
        self.contname = 'testcont01'
        self.r = iori.repo.Repo(self.dirpath)

    def test__init__(self):
        self.assertEquals('/tmp/iori_test', self.r.dirpath)
        self.assertIsNone(self.r.git_repo)
        self.assertFalse(self.r.contname)
