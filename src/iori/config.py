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
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


class Config(object):
    def __init__(self):
        # vm1
        self.contname = ''
        # default 64MB
        self.memory = '64000'
        # '/sbin/init' | '/bin/sh'
        self.os_init = '/bin/sh'
        # default 1
        self.vcpu = '1'
        # default utc
        self.clock_offset = 'utc'
        # default is 'default'
        self.network = 'default'
        # specify root fs path under /var/lib/lxc/$(contname),
        # when using debootstrap, default is Null
        self.rootfs = None

    def generateXML(self):
        if not self.contname:
            sys.stderr.write('ERROR: not allow container name is null\n')
        else:
            # top element
            e_domain = Element('domain', {'type': 'lxc'})

            # vm name
            e_name = SubElement(e_domain, 'name')
            e_name.text = self.contname

            # memory size
            e_memory = SubElement(e_domain, 'memory')
            e_memory.text = self.memory

            # os definition
            e_os = SubElement(e_domain, 'os')

            e_type = SubElement(e_os, 'type')
            e_type.text = 'exe'

            e_init = SubElement(e_os, 'init')
            if self.rootfs and os.path.isdir(self.rootfs):
                self.os_init = '/sbin/init'
            e_init.text = self.os_init

            e_vcpu = SubElement(e_domain, 'vcpu')
            e_vcpu.text = self.vcpu

            e_clock = SubElement(e_domain, 'clock',
                                 {'offset': self.clock_offset})

            e_on_poweroff = SubElement(e_domain, 'on_poweroff')
            e_on_poweroff.text = 'destroy'

            e_on_reboot = SubElement(e_domain, 'on_reboot')
            e_on_reboot.text = 'restart'

            e_on_crash = SubElement(e_domain, 'on_crash')
            e_on_crash.text = 'destroy'

            e_devices = SubElement(e_domain, 'devices')
            e_emulator = SubElement(e_devices, 'emulator')
            e_emulator.text = '/usr/lib/libvirt/libvirt_lxc'

            # rootfs for debootstrap
            if self.rootfs and self.os_init == 'init':
                e_filesystem = SubElement(e_devices, 'filesystem',
                                          {'type': 'mount'})
                e_source = SubElement(e_filesystem, 'source',
                                      {'dir': self.rootfs})
                e_target = SubElement(e_filesystem, 'target',
                                      {'dir': '/'})

            # network
            e_interface = SubElement(e_devices, 'interface',
                                     {'type': 'network'})
            e_interface_source = SubElement(e_interface, 'source',
                                            {'network': self.network})
            e_console = SubElement(e_devices, 'console', {'type': 'pty'})

            return tostring(e_domain)
