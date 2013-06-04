# -*- coding: utf-8 -*-

"""
Tests of repo.py
"""
import unittest
import sys
import os.path
sys.path.append(os.path.abspath('src'))
import iori.repo
import iori_tests.test_vars as v


class RepoTests(unittest.TestCase):
    def setUp(self):
        self.r = iori.repo.lxcRepo(v.dirpath)

    def test__init__(self):
        self.assertEquals(v.dirpath, self.r.dirpath)
        self.assertIsNone(self.r.git_repo)

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
