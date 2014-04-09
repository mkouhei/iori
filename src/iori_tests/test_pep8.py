# -*- coding: utf-8 -*-
import os
import unittest
import pep8

BASE_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


class PEP8Test(unittest.TestCase):
    def test_pep8(self):
        pep8.DEFAULT_EXCLUDE = '.tox,*.egg,_build/'
        pep8style = pep8.StyleGuide([['statistics', True],
                                     ['show-sources', True],
                                     ['repeat', True],
                                     ['paths', [BASE_PATH]]],
                                    parse_argv=False,
                                    config_file=True)
        report = pep8style.check_files()
        assert report.total_errors == 0
