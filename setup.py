#!/usr/bin/env python
# Copyright (C) 2012, 2013 Enrico Rossi
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
from glob import glob
import os

setup(name='blueshop',
        version='2.0',
        description='Yet Another small web shop',
        author='Enrico Rossi',
        author_email='e.rossi@tecnobrain.com',
        url='http://enricorossi.org/blueshop/',
        packages=['blueshop'],
        package_dir={'blueshop': 'bin'},
        scripts=['bin/blueshop'],
        data_files=[
            ('/var/local/blueshop/db', ['db/users.sqlite3.dump',
                'db/shop.sqlite3.dump']),
            ('/var/local/blueshop/private', ['private/stock.xls',
                'private/vip.xls', 'private/eu.xls']),
            ('etc/blueshop', ['cfg/blueshop.cfg',
                'cfg/mail_pricelist.txt',
                'cfg/mail_promo.txt']),
            ('share/blueshop/views',
                glob(os.path.join('bin/views', '*.tpl'))),
            ('share/blueshop/views/admin',
                glob(os.path.join('bin/views/admin', '*.tpl'))),
            ('share/blueshop/views/mail',
                glob(os.path.join('bin/views/mail', '*.tpl'))),
            ('share/blueshop/views/main',
                glob(os.path.join('bin/views/main', '*.tpl'))),
            ('share/blueshop/views/store',
                glob(os.path.join('bin/views/store', '*.tpl'))),
            ('share/blueshop/views/user',
                glob(os.path.join('bin/views/user', '*.tpl'))),
            ('share/blueshop/images',
                glob(os.path.join('bin/images', '*.png'))),
            ('share/blueshop/static',
                glob(os.path.join('bin/static', 'x*'))),
            ('share/blueshop/static/javascripts',
                glob(os.path.join('bin/static/javascripts', '*.js'))),
            ('share/blueshop/static/stylesheets',
                glob(os.path.join('bin/static/stylesheets', '*.css'))),
            ('share/doc/blueshop',
                glob(os.path.join('doc', '*.txt'))),
            ('share/doc/blueshop/example',
                glob(os.path.join('doc/example', '*')))
            ])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
