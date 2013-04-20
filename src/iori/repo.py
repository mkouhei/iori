# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012 Kouhei Maeda <mkouhei@palmtb.net>

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
import glob
import git


class lxcRepo(object):

    def __init__(self, dirpath):
        self.dirpath = os.path.abspath(dirpath) + '/'

        # instantication
        self.git_cmd = git.cmd.Git(self.dirpath)
        if git.repo.fun.is_git_dir(self.dirpath + '/.git'):
            self.git_repo = git.repo.Repo(self.dirpath)
        else:
            self.git_repo = None
        #self.git_index = git.IndexFile(self.git_repo)

        # container name
        self.contname = ''

    def check_dirrepo(self):
        # if not exist dir, then mkdir local repository
        if not os.path.isdir(self.dirpath):
            print("ERROR: %s such not directory" % self.dirpath)
            exit(1)

        # git init when not git repository
        if not self.git_repo:
            print("ERROR: %s such not repository" % self.git_repo)
            exit(1)

    def write_file(self, filename, msg=''):
        with open(filename, 'w') as f:
            f.write(msg)

    # when git init once only
    def git_init(self):
        # if not exist dir, then mkdir local repository
        if not os.path.isdir(self.dirpath):
            os.makedirs(self.dirpath)

        # git init when not git repository
        if not self.git_repo:
            self.git_cmd.init()
            self.git_repo = git.repo.Repo(self.dirpath)

            # first commit to master branch
            gitignore = (self.dirpath + '/.gitignore')
            self.write_file(gitignore)
            self.git_add_commit(gitignore)

            # make a new template branch from master
            self.make_branch('template')
            self.checkout_branch('template')

            # generate README
            readme = (self.dirpath + '/README')
            msg = ('This repository is generate automatically by iori.\n'
                   '"master" branch is mapping of relation '
                   'lxc host node and git ripository\n'
                   'branches. Other branches exception of '
                   'master and template are created by\n'
                   'every lxc host from "template" branch.\n')
            self.write_file(readme, msg)
            self.git_add_commit(readme)
            self.checkout_branch('master')

        else:
            d = self.dirpath.__str__()
            print('ERROR: "%s" is already existed' % d)

    def git_add_commit(self, filename):
        # git add
        self.git_cmd.add(filename)

        # generate commit message
        if self.git_cmd.untracked_files:
            action = 'add '
        elif self.git_cmd.is_dirty():
            action = 'update '

        if self.contname:
            msg = self.contname + ': ' + action + os.path.basename(filename)
        else:
            msg = action + os.path.basename(filename)

        # git commit
        self.git_cmd.commit(m=msg)

    def make_branch(self, branch_name):
        self.check_dirrepo()

        # If already repository is existed, create from template branch
        if 'template' in self.git_repo.branches:
            self.checkout_branch('template')

        self.git_repo.create_head(branch_name)

    def checkout_branch(self, branch_name):
        self.check_dirrepo()

        # clean working tree
        self.git_repo.active_branch.checkout()

        # checkout specific branch
        self.git_cmd.checkout(branch_name)

    def branches(self):
        self.check_dirrepo()
        print("no\tnode name")
        print("=" * 39)

        for i, branch in enumerate(self.git_repo.branches):
            if not ((str(branch) == 'master') or (str(branch) == 'template')):
                print("%d:\t%s" % (i, branch))

    def branch_files(self):
        self.check_dirrepo()

        nodes = []
        for branch in self.git_repo.branches:
            containers = []
            if not ((str(branch) == 'master') or (str(branch) == 'template')):
                # checkout branch
                self.git_cmd.checkout(branch)

                # get managed files
                files = self.git_cmd.ls_files()

                if files:
                    for file in files.split('\n'):
                        if 'xml' in file:
                            contname = file.split('.xml')[0]
                            containers.append({'contname': contname})
                nodes.append({'node': str(branch), 'cont': containers})
        return nodes

    def git_rm_commit(self, contname):
        # git rm
        filename = contname + '.xml'
        try:
            self.git_cmd.rm(filename)
        except git.exc.GitCommandError as e:
            pass

        # generate commit message
        action = 'delete '
        msg = action + filename

        # git commit
        self.git_cmd.commit(m=msg)
