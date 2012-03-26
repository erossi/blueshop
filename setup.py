#!/usr/bin/env python
# Copyright (C) 2012 Enrico Rossi
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

setup(name='blueshop',
        version='2.0',
        description='Yet Another small web shop',
        author='Enrico Rossi',
        author_email='e.rossi@tecnobrain.com',
        url='http://enricorossi.org/blueshop/',
        packages=['blueshop'],
        package_dir={'blueshop': 'bin'},
#        data_files=[('var/lib/blueshop', ['db/users.sqlite3']),
#            ('var/lib/blueshop', ['db/shop.sqlite3'])],
        )

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4ys directory tree, in color
