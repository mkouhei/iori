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
import sys
import os.path
import subprocess


# this module is wrapper of debootstrap, then is is named 'debootstwrap' :)
class Debootstrap(object):

    def __init__(self, nodename, rootfs):
        cmd_exe = '/usr/bin/cdebootstrap'
        if not os.path.isfile(cmd_exe):
            sys.stderr.write("ERROR: %s is not existed. \
Install %s package.\n" % (cmd_exe, str(os.path.basename(cmd_exe))))

        if nodename in ('127.0.0.1', 'localhost',
                        '::1', 'ip6-localhost', 'ip6-loopback'):
            self.target = rootfs
        else:
            self.target = nodename + ':' + rootfs
        dist = 'squeeze'
        arch = 'amd64'
        uri = 'http://cdn.debian.net/debian/'
        flavour = 'minimal'
        include = 'ifupdown,locales,libui-dialog-perl,dialog,isc-dhcp-client,'
        'netbase,net-tools,iproute,oepnssh-server,lv,git,etckeeper,sudo'
        # cdebootstrap command and arguments
        self.cmd = [cmd_exe,
                    '--flavour=%s' % flavour,
                    '--include=%s' % include,
                    dist,
                    rootfs,
                    '--arch=%s' % arch,
                    uri]

        self.inittab = '''id:3:initdefault:
si::sysinit:/etc/init.d/rcS
l0:0:wait:/etc/init.d/rc 0
l1:1:wait:/etc/init.d/rc 1
l2:2:wait:/etc/init.d/rc 2
l3:3:wait:/etc/init.d/rc 3
l4:4:wait:/etc/init.d/rc 4
l5:5:wait:/etc/init.d/rc 5
l6:6:wait:/etc/init.d/rc 6
z6:6:respawn:/sbin/sulogin
1:2345:respawn:/sbin/getty 38400 console
c1:12345:respawn:/sbin/getty 38400 tty1 linux
c2:12345:respawn:/sbin/getty 38400 tty2 linux
c3:12345:respawn:/sbin/getty 38400 tty3 linux
c4:12345:respawn:/sbin/getty 38400 tty4 linux
'''

    def debootstrap(self):
        if not os.path.isdir(self.target):
            subprocess.Popen(['sudo', self.cmd])

            # touch /etc/fstab
            f = open(self.rootfs + '/etc/fstab', 'w')
            f.write('')
            f.close()

            # override /etc/inittab
            f = open(self.rootfs + '/etc/inittab', 'w')
            f.write(self.inittab)
            f.close()
