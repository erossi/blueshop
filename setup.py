#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2012-2014 Enrico Rossi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
from distutils.command.sdist import sdist
from glob import glob
import os
import fnmatch
from subprocess import call

# Update the version needed also for the package name.
# FIXME isn't any other better way to do this?
if call('tools/update_version.sh', shell=True):
    print('Error updating version.')

from modules import _version_

class SdistOverride(sdist):
    """ Useless now that the updated version is called before
    """
    def run(self):
        print('Updating version from git.')

        if call('tools/update_version.sh', shell=True):
            print('Error updating version.')
        else:
            sdist.run(self)

def select_all_files(folder, matchfilter):
    """ Scan subdirectory and select all the matching files.

    Return: a list of tuple compatibile with the setup list.
    """
    result = []

    for root, dirnames, filenames in os.walk(folder):
        selected_files = []

        for filename in fnmatch.filter(filenames, matchfilter):
            selected_files.append(os.path.join(root, filename))

        if len(selected_files):
            result.append((root, selected_files))

    return (result)

def list_data_files():
    """ Create the data_files list for setup.
    """
    data_files = [
        ('/var/lib/blueshop/db', glob(os.path.join('./db', '*.dump'))),
        ('/var/lib/blueshop/private', ['private/stock.xls',
            'private/vip.xls', 'private/eu.xls']),
        ('/etc/blueshop', ['cfg/blueshop.cfg', 'cfg/mail_pricelist.txt',
            'cfg/mail_promo.txt', 'cfg/blueshop.vhost']),
        ('images', ['images/favicon.ico']),
        ('static', glob(os.path.join('./static', 'x*'))),
        ('static/javascripts',
            glob(os.path.join('./static/javascripts', '*.js'))),
        ('static/stylesheets',
            glob(os.path.join('./static/stylesheets', '*.css'))),
        ('/usr/share/doc/blueshop',
            glob(os.path.join('doc', '*.txt'))),
        ('/usr/share/doc/blueshop/example',
            glob(os.path.join('doc/example', '*')))
        ]

    data_files += select_all_files('views', '*.tpl')
    data_files += select_all_files('images', '*.png')
    data_files += select_all_files('images', '*.gif')
    data_files += select_all_files('locale', '*.mo')
    # print 'data_files = ', data_files
    return(data_files)

setup(name='blueshop',
        version=_version_,
        description='Yet Another small web shop',
        author='Enrico Rossi',
        author_email='e.rossi@tecnobrain.com',
        url='http://enricorossi.org/blueshop/',
        packages=['blueshop'],
        package_dir={'blueshop': 'modules'},
        data_files=list_data_files(),
        )
#        cmdclass={'sdist':SdistOverride})

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
