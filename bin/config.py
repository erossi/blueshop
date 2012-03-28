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

import os
import time
import ConfigParser

class Config:
    """
    Default configurations.
    """

    if os.getenv('BLUESHOP_CFG'):
        _config_path = (os.getenv('BLUESHOP_CFG'),)
    else:
        _config_path = ('/etc/blueshop',
                '/usr/local/etc/blueshop',
                '~/.blueshop',
                './cfg')

    print "Configurations path: " + str(_config_path)

    config = None
    path = {}
    db = {}
    users = {}
    pricelists = {}
    promo = {}
    mail = {}

    pricelists['email_text'] = None
    promo['email_text'] = None
    
    # these are automatically updated, don't touch
    pricelists['file1'] = None
    pricelists['file2'] = None
    pricelists['file3'] = None
    pricelists['mtime_pl1'] = None
    pricelists['mtime_pl2'] = None
    pricelists['mtime_pl3'] = None

    def _read_config(self, cfgpath):
        filename = os.path.join(cfgpath, 'blueshop.cfg')

        if os.path.isfile(filename):
            self.config.read(filename)
            self.path = dict(self.config.items('path'))
            self.db = dict(self.config.items('db'))
            self.users = dict(self.config.items('users'))
            self.pricelists = dict(self.config.items('pricelists'))
            self.promo = dict(self.config.items('promo'))
            self.mail = dict(self.config.items('mail'))
            # fix bcc from str to int
            self.mail['bcc_limit'] = int(self.mail['bcc_limit'])

    def _read_mail_text(self, cfgpath):
        filename = os.path.join(cfgpath, 'mail_pricelist.txt')

        if os.path.isfile(filename):
            f = open(filename, 'r')
            self.pricelists['email_text'] = f.read()
            f.close()

        filename = os.path.join(cfgpath, 'mail_promo.txt')

        if os.path.isfile(filename):
            f = open(filename, 'r')
            self.promo['email_text'] = f.read()
            f.close()

    def update_filenames(self):
        self.pricelists['file1'] = os.path.join(self.path['private'],
                self.pricelists['filename1'])
        self.pricelists['file2'] = os.path.join(self.path['private'],
                self.pricelists['filename2'])
        self.pricelists['file3'] = os.path.join(self.path['private'],
                self.pricelists['filename3'])

    def update_mtime(self):
        # file 1
        mtime = os.stat(self.pricelists['file1']).st_mtime
        self.pricelists['mtime_pl1'] = time.strftime('%Y-%m-%d %H:%M:%S',
                time.localtime(mtime))
        # file 2
        mtime = os.stat(self.pricelists['file2']).st_mtime
        self.pricelists['mtime_pl2'] = time.strftime('%Y-%m-%d %H:%M:%S',
                time.localtime(mtime))
        # file 3
        mtime = os.stat(self.pricelists['file3']).st_mtime
        self.pricelists['mtime_pl3'] = time.strftime('%Y-%m-%d %H:%M:%S',
                time.localtime(mtime))

    def update_config(self):
        for cfgpath in self._config_path:
            if os.path.isdir(cfgpath):
                self._read_config(cfgpath)
                self._read_mail_text(cfgpath)

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.update_config()
        self.update_filenames()

if __name__ == "__main__":
    print "Cannot execute as program!"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
