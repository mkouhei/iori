# -*- coding: utf-8 -*-
"""
    Copyright (C) 2012, 2013 Kouhei Maeda <mkouhei@palmtb.net>

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
import sys
import os.path
import libvirt as l


class Controller(object):
    def __init__(self, nodename):
        self.node = nodename
        self.conn = False
        self.xml = ''
        self.user = None
        self.domname = None
        self.dirname = ''
        self.connect()

    # connect libvirtd
    def connect(self):
        try:
            if self.node == 'localhost' or self.node == 'ip6-localhost':
                self.conn = l.open('lxc:///')
            else:
                # enable to specify user account is belong to libvirt group
                if not self.user:
                    self.user = 'root'
                self.conn = l.open('lxc+ssh://' +
                                   self.user + '@' + self.node + '/')
        except l.libvirtError as error:
            print("ERROR: %s" % error)

    # list network
    def net_list_of_node(self):
        return dict(defined=self.conn.listDefinedNetworks(),
                    active=self.conn.listNetworks(),
                    network=self.conn.networkLookupByName('default').name())

    # get defined xml description
    def getContainerDefinedXML(self, dom):
        return dom.XMLDesc(0)

    # write xml file
    def saveDefinedXML(self, dirpath, xml):
        if os.path.isdir(dirpath):
            xmlfile = dirpath + self.domname + '.xml'
        else:
            sys.stderr('ERROR')
            exit(1)
        with open(xmlfile, 'w') as f:
            f.write(xml)
        return os.path.basename(xmlfile)

    def createTemporaryContainer(self):
        # lxc is enable to use flag that is 0 or 2
        # 0 is enable to boot from python script and python shell
        # 2 is unable to boot from python script,
        # but enable to boot with python shell.
        # temporary create, then shutdown and remove
        # So this method is for temporary instance
        self.conn.createXML(self.xml, 0)

    def defineContainer(self):
        # define dom and shut off
        self.conn.defineXML(self.xml)

    def undefineContainer(self, dom):
        dom.undefine()

    def getState(self, dom):
        dom.state(0)

    def startContainer(self, dom):
        # change state: 1
        dom.create()

    '''
    def shutdownContainer(self, dom):
        # change state: 5
        # this function is not supported by the connection driver:
        #  -> virDomainShutdown
        dom.shutdown()
        '''

    def destoryContainer(self, dom):
        # change state: 5
        # this function is not supported by the connection driver:
        #  -> virDomainShutdown
        dom.destroy()

    def suspendContainer(self, dom):
        # change state: 3
        dom.suspend()

    def resumeContainer(self, dom):
        # change state: 1
        dom.resume()

    '''
    def rebootContainer(self, dom):
    # this function is not supported by the connection driver: virDomainReboot
        dom.reboot(1)
        '''

    '''
    def resetContainer(self, dom):
    # this function is not supported by the connection driver: virDomainReset
        dom.reset(0)
        '''

    def getDomObj(self):
        for id in self.conn.listDomainsID():
            dom = self.conn.lookupByID(id)
            if self.domname == dom.name():
                return dom
        if self.domname in self.conn.listDefinedDomains():
            dom = self.conn.lookupByName(self.domname)
            return dom
        else:
            return False

    def list(self):
        doms = []
        for id in self.conn.listDomainsID():
            dom = self.conn.lookupByID(id)
            # dom.info()
            # 0:state, 1:mem, 2:?, 3:?, 4:?
            # state: 1: running, 5: shut off
            # mem: KB ('L' is long?)
            # ?: 676L
            # ?: 1
            # ?: 15940056L
            doms.append({'domname': dom.name(),
                         'state': self.state(dom.info()[0]),
                         'defined': False})

        for defined_id in self.conn.listDefinedDomains():
            defined_dom = self.conn.lookupByName(defined_id)
            doms.append({'domname': defined_dom.name(),
                         'state': self.state(defined_dom.info()[0]),
                         'defined': True})
        return doms

    def state(self, flag):
        if flag == 1:
            return "running"
        elif flag == 5:
            return "shut off"
