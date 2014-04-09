# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012-2014 Kouhei Maeda <mkouhei@palmtb.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import multiprocessing

sys.path.insert(0, 'src')
import iori


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: "
    "GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python",
    "Topic :: System :: Systems Administration",
]

long_description = (open(os.path.join("docs", "README.rst")).read() +
                    open(os.path.join("docs", "HISTORY.rst")).read() +
                    open(os.path.join("docs", "TODO.rst")).read())

requires = ['setuptools',
            'lxml',
            'defusedxml',
            'GitPython',
            'libvirt-python']


setup(name='iori',
      version=iori.__version__,
      description='LXC deploy and config management tool',
      long_description=long_description,
      author='Kouhei Maeda',
      author_email='mkouhei@palmtb.net',
      url='https://github.com/mkouhei/iori',
      license=' GNU General Public License version 3',
      classifiers=classifiers,
      packages=find_packages('src'),
      package_dir={'': 'src'},
      data_files=[],
      install_requires=requires,
      tests_require=['tox'],
      cmdclass={'test': Tox},
      entry_points="""
        [console_scripts]
        iori = iori.command:main
      """,)
