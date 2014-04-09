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
import os.path
import argparse
from __init__ import __version__
import control


def parse_options():
    prs = argparse.ArgumentParser(description='usage')
    prs.add_argument('-V', '--version', action='version', version=__version__)
    setoption(prs, 'dirpath')
    subprs = prs.add_subparsers(help='commands')

    # Make repository
    prs_make_repo(subprs)

    # Add new node
    prs_add_node(subprs)

    # Create container
    prs_create_container(subprs)

    # Start container
    prs_start_container(subprs)

    # Shutdown container ; not yet supported
    # prs_shutdown_container(subprs)

    # destroy container
    prs_destroy_container(subprs)

    # Delete container
    prs_delete_container(subprs)

    # Listing nodes
    prs_list_nodes(subprs)

    # Listing defined containers
    prs_list_containers(subprs)

    args = prs.parse_args()
    return args


# Make repository
def prs_make_repo(obj):
    prs_make_repo = obj.add_parser('newrepo', help='make new repository')
    setoption(prs_make_repo, 'dirpath')
    prs_make_repo.set_defaults(func=make_repo)


# Add new node
def prs_add_node(obj):
    prs_add_node = obj.add_parser('addnode', help='add new lxc host node')
    setoption(prs_add_node, 'nodename')
    prs_add_node.set_defaults(func=add_node)


# Create container
def prs_create_container(obj):
    prs_create_container = obj.add_parser('deploy',
                                          help='create lxc container')
    setoption(prs_create_container, 'nodename')
    setoption(prs_create_container, 'contname')
    setoption(prs_create_container, 'vcpu')
    setoption(prs_create_container, 'memory')
    setoption(prs_create_container, 'clock')
    setoption(prs_create_container, 'network')
    setoption(prs_create_container, 'rootfs')
    setoption(prs_create_container, 'debootstrap')
    prs_create_container.set_defaults(func=create_container)


# Start container
def prs_start_container(obj):
    prs_start_container = obj.add_parser('start',
                                         help='start lxc container')
    setoption(prs_start_container, 'nodename')
    setoption(prs_start_container, 'contname')
    prs_start_container.set_defaults(func=start_container)

'''
# Shutdown container; not yet supported by libvirt
def prs_shutdown_container(obj):
    prs_shutdown_container = obj.add_parser('shutdown',
                                          help='shutdown lxc container')
    setoption(prs_shutdown_container, 'nodename')
    setoption(prs_shutdown_container, 'contname')
    prs_shutdown_container.set_defaults(func=shutdown_container)
    '''


# Destroy container
def prs_destroy_container(obj):
    prs_destroy_container = obj.add_parser('destroy',
                                           help='destroy lxc container')
    setoption(prs_destroy_container, 'nodename')
    setoption(prs_destroy_container, 'contname')
    prs_destroy_container.set_defaults(func=destroy_container)


# Delete(undefine) container
def prs_delete_container(obj):
    prs_delete_container = obj.add_parser('delete',
                                          help='delete lxc container')
    setoption(prs_delete_container, 'nodename')
    setoption(prs_delete_container, 'contname')
    prs_delete_container.set_defaults(func=delete_container)


# Listing nodes
def prs_list_nodes(obj):
    prs_list_nodes = obj.add_parser('listnode',
                                    help='listing nodes')
    prs_list_nodes.set_defaults(func=list_nodes)


# Listing defined containers
def prs_list_containers(obj):
    prs_list_containers = obj.add_parser('listcont',
                                         help='listing containers')
    setoption(prs_list_containers, 'nodename')
    prs_list_containers.set_defaults(func=list_containers)


def setoption(obj, kword):
    if kword == 'dirpath':
        obj.add_argument('-d', '--dirpath', action='store',
                         help='specify repository path')
    elif kword == 'nodename':
        obj.add_argument('-n', '--nodename', action='store', required=True,
                         help='hostname or IP address of lxc host node')
    elif kword == 'contname':
        obj.add_argument('-c', '--contname', action='store', required=True,
                         help='container name')
    elif kword == 'vcpu':
        obj.add_argument('--vcpu', action='store',
                         help='vcpu number / default: 1')
    elif kword == 'memory':
        obj.add_argument('--mem', action='store',
                         help='memory size / default: 64000(KB)')
    elif kword == 'clock':
        obj.add_argument('--clock', action='store',
                         help='clock / default: utc')
    elif kword == 'network':
        obj.add_argument('--network', action='store',
                         help='network type/ default: default')
    elif kword == 'rootfs':
        obj.add_argument(
            '--rootfs', action='store_true',
            help='create rootfs path to /var/lib/lxc/$(contname)')
    elif kword == 'debootstrap':
        obj.add_argument(
            '--debian', action='store_true',
            help='create rootfs image with debootstrap')


def repopath(args):
    if args.__dict__.get('dirpath'):
        dirpath = args.__dict__.get('dirpath')
    else:
        dirpath = os.path.abspath(os.environ['HOME'] + '/.iori') + '/'
    return dirpath


def nodename(args):
    if args.__dict__.get('nodename'):
        nodename = args.__dict__.get('nodename')
    else:
        nodename = 'localhost'
    return nodename


def make_repo(args):
    ctl = control.Control(repopath(args))
    ctl.make_repo()


def add_node(args):
    if args.__dict__.get('nodename'):
        nodename = args.__dict__.get('nodename')
    ctl = control.Control(repopath(args))
    ctl.add_node(nodename)


def create_container(args):
    ctl = control.Control(repopath(args), nodename(args))
    ctl.create_container(args)


def start_container(args):
    ctl = control.Control(repopath(args), nodename(args))
    ctl.start_container(args)


def list_nodes(args):
    ctl = control.Control(repopath(args))
    ctl.list_nodes()


def list_containers(args):
    ctl = control.Control(repopath(args), nodename(args))
    ctl.list_containers(args)


'''
def shutdown_container(args):
    ctl = control.Control(repopath(args))
    ctl.delete_container(args)
    '''


def destroy_container(args):
    ctl = control.Control(repopath(args), nodename(args))
    ctl.destroy_container(args)


def delete_container(args):
    ctl = control.Control(repopath(args), nodename(args))
    ctl.delete_container(args)


def print_error(error):
    print("ERROR: %s" % error)


def main():
    try:
        args = parse_options()
        args.func(args)
    except RuntimeError as error:
        print_error(error)
        return
    except UnboundLocalError as error:
        print_error(e)
        return


if __name__ == '__main__':
    main()
