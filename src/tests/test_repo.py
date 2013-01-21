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
        self.r = iori.repo.lxcRepo(self.dirpath)

    def test__init__(self):
        self.assertEquals('/tmp/iori_test/', self.r.dirpath)
        self.assertIsNone(self.r.git_repo)
        self.assertFalse(self.r.contname)

    '''
    def test_check_dirrepo(self):
        unittest.TextTestRunner().run(self.r.check_dirrepo())
        '''

    def test_write_file(self):
        True

    def test_git_init(self):
        True

    def test_git_add_commit(self):
        True

    def test_make_branch(self):
        True

    def test_checkout_branch(self):
        True

    def test_branches(self):
        True

    def test_branch_files(self):
        True

    def git_rm_commit(self):
        True
