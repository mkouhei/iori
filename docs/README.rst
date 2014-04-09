=====================================================
Iori is LXC deploying and config management tool.
=====================================================

What's "Iori"?
--------------

"Iori" is means a simple hut. It is written "庵" in Kanji, this caracter is 0x5EB5 in Unicode.
 
Iori is a command line tool for deploying and config management tool of Linux Containers (LXC). When you use LXC, you need to use LXC userland command line tool as start with "lxc-\*" generally. LXC is provided template config file and scripts. But this way if you want to manage from a remote contoller host is difficult to treat containers by bulk. So this tool controls LXC with libvirt API, and manages these config files with Git repository.

This tool is enable to manage LXC container's multi hosts. It is that one branch is managed as one host. Branch name is generated from hostname(or FQDN) or IPv4 or IPv6 address. 'master' branch will be using for mapping. 'template' branch is used for template of each node.

Requirements
------------

* Python 2.7
* python-libvirt (0.9.12)
* GitPython (0.3.2-rc1)
* cdebootstrap (not test of debootstrap)

You do not need to install lxc package. :)

Setup
-----

Mount cgroup file system
^^^^^^^^^^^^^^^^^^^^^^^^

Mount cgroup filesystem firstly. Append next one line to /etc/fstab, execute "sudo mount -a."::

  cgroup /sys/fs/cgroup cgroup defaults 0 0
 

If you use Debian GNU/Linux Wheezy/Sid, set up below option to /etc/default/grub, then execute "sudo update-grub2 && sudo shutdown -r now".::

  GRUB_CMDLINE_LINUX="cgroup_enable=memory"

Ubuntu 12.04 is unnecessary to setup this option.


Install Debian packages that Iori depends on
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iori depends on GitPython, python-libvirt and libvirt, and Python2.7. Install these packages.::

  $ sudo apt-get install python-git libvirt-bin python-libvirt


Install Iori
^^^^^^^^^^^^

Install that choosing with one of three ways.

from source
"""""""""""
::

   $ git clone https://github.com/mkouhei/iori.git
   $ cd iori
   $ sudo python setup.py install


PyPI
""""
::

   $ pip install iori

Debian package 
""""""""""""""

Not yet official package, then download python-iori-x.x_all.deb from https://github.com/mkouhei/iori/downloads and install with dpkg command.::

  $ wget https://github.com/mkouhei/iori/download/python-iori_x.x-x_all.deb
  $ sudo dpkg -i python-iori_x.x-x_all.deb


Add a user account to libvirt(libvirtd) group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add a user account for using iori to libvirt  or libvirtd group.::

  $ sudo adduser <youraccount> libvirt

libvirt is for Debian, libvirtd is for Ubuntu.


Make direcotry
^^^^^^^^^^^^^^

If directory "/var/lib/lxc" is not existed, make it.::

  $ sudo mkdir /var/lib/lxc


Quick start guide
-----------------

Create repository
^^^^^^^^^^^^^^^^^

Create $HOME/.iori directory and initialize Git repository. ::

  $ iori newrepo

Add LXC host node to Git repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make branch of named hostname of LXC host node, checktout it.::

  $ iori addnode -n localhost

Define libvirt XML file and create rootfs image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate XML file of libvirt domain, and define domain from this xml, create rootfs image with debootstrap command. Then save XML file of that domain.::

  $ iori deploy -n localhost -c testcont01 --rootfs /var/lib/lxc/testcont01


Start container
^^^^^^^^^^^^^^^

Start container from above domain.::

  $ iori start -n localhost -c testcont01


Development
-----------

You copy pre-commit hook scripts after git clone.::

  $ cp -f utils/pre-commit.txt .git/hooks/pre-commit

Next install python 2.7 later and setuptools, pep8, libvirt, libvirt-dev, python-libvirt, GitPython, cdebootstrap, python-tox, python-virtualenv. Below way is for Debian GNU/Linux Sid system.::

  $ sudo apt-get install python python-libvirt python-git python-setuptools pep8 libvirt-dev python-tox python-virtualenv

Then checkout 'devel' branch for development, commit your changes. Before pull request, execute git rebase.

See also
--------

* `lxc Linux Containers <http://lxc.sourceforge.net/>`_
* `libvirt The virtualization API <http://libvirt.org/>`_
* `GitPython <http://packages.python.org/GitPython/0.3.2/>`_
* `ElementTree XML API <http://www.python.jp/doc/release/library/xml.etree.elementtree.html?highlight=xml.etree.elementtree#xml.etree.ElementTree>`_ 
* `Appendix D. Random Bits - D.3. Installing Debian GNU/Linux from a Unix/Linux System <http://www.debian.org/releases/stable/amd64/apds03.html>`_

See also these documents.
