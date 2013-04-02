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
import git
import repo
import config
import libvirtobj
import debootstwrap


class Control(object):

    def __init__(self, dirpath, node=''):
        self.r = repo.lxcRepo(dirpath)
        if node:
            self.l = libvirtobj.Controller(node)
        self.c = config.Config()
        self.dirpath = dirpath

    def make_repo(self):
        # make repository
        self.r.git_init()

    def add_node(self, nodename):
        self.r.make_branch(nodename)
        self.r.checkout_branch(nodename)

    def create_container(self, param):
        if param.nodename:
            nodename = param.nodename
            try:
                self.r.checkout_branch(nodename)
            except git.exc.GitCommandError:
                print('ERROR: %s: No such node' % nodename)

        self.c.contname = param.contname

        if param.__dict__.get('vcpu'):
            self.c.vcpu = param.vcpu

        if param.__dict__.get('memory'):
            self.c.memory = param.memory

        if param.__dict__.get('clock'):
            self.c.clock = param.clock

        if param.__dict__.get('network'):
            self.c.network = param.network

        if param.__dict__.get('rootfs'):
            rootfs = '/var/lib/lxc/' + self.c.contname
            if param.__dict__.get('debootstrap'):
                d = debootstwrap.Debootstrap(nodename, rootfs)
                d.debootstrap()

        # generate XML strings
        self.l.xml = self.c.generateXML()

        if param.__dict__.get('rootfs'):
            # get domname
            self.l.domname = param.contname

            # get defined domain object
            dom = self.l.getDomObj()
            if not dom:
                # create permanent container
                self.l.defineContainer()

                # get domain objenct after create domain
                dom = self.l.getDomObj()

            # get defined XML strings
            xml = self.l.getContainerDefinedXML(dom)

            # write XML file
            xmlname = self.l.saveDefinedXML(self.dirpath, xml)

            # git add and commit XML file
            self.r.git_add_commit(xmlname)
        else:
            # create temporary container
            self.l.createTemporaryContainer()

    def list_nodes(self):
        self.r.branches()

    def list_containers(self, param):
        for node in self.r.branch_files():
            if node.get('node') == param.nodename:
                print('nodename:\t%s' % node.get('node'))
        print('%-20s%-10s%-10s' % ('container', 'state', 'defined'))
        print('-' * 40)
        for dom in self.l.list():
            print('%-20s%-10s%-10s' %
                  (dom.get('domname'), dom.get('state'), dom.get('defined')))

    def start_container(self, param):
        if param.__dict__.get('nodename'):
            try:
                self.r.checkout_branch(param.nodename)
            except git.exc.GitCommandError:
                print('ERROR: %s: No such node' % param.nodename)

        self.l.domname = param.contname

        # get defined domain object
        dom = self.l.getDomObj()

        if dom:
            # start container
            self.l.startContainer(dom)

    def destroy_container(self, param):
        if param.__dict__.get('nodename'):
            try:
                self.r.checkout_branch(param.nodename)
            except git.exc.GitCommandError:
                sys.stderr.write('ERROR: %s: No such node\n' %
                                 param.nodename)

        self.l.domname = param.contname

        # get defined domain object
        dom = self.l.getDomObj()

        if dom:
            # destroy container
            self.l.destoryContainer(dom)
            # self.l.shutdownContainer(dom)

    def delete_container(self, param):
        if param.__dict__.get('nodename'):
            try:
                self.r.checkout_branch(param.nodename)
            except git.exc.GitCommandError:
                sys.stderr.write('ERROR: %s: No such node\n' %
                                 param.nodename)

        self.l.domname = param.contname

        # get defined domain object
        dom = self.l.getDomObj()

        if dom:
            # create permanent container
            self.l.undefineContainer(dom)

        # git rm and commit XML file
        self.r.git_rm_commit(param.contname)
