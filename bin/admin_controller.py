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


import csv
import string
import time
from bottle import template

class Admin:
    """
    The Admin class.
    
    Functions for the admin menu.
    """

    # Local object of the shop model
    _shopdb = None
    # configuration parameters
    _config = None

    def __init__(self, shopdb, config):
        self._shopdb = shopdb
        self._config = config

    def index(self, cookie):
        myuser = cookie[0]
        pdata = {'user':myuser, 'cat':self._shopdb.categories,
                'error':None, 'notice':None}
        return template('admin/index', tpldata=pdata)

    def items(self, cookie, flash=None):
        myuser = cookie[0]
        dcat = cookie[1]
        articles = self._shopdb.get_all_items(dcat);
        pdata = {'user':myuser, 'cat':self._shopdb.categories,
                'defcat':dcat, 'articles':articles, 'flash':flash}
        return template('admin/items', tpldata=pdata)

    def item_remove(self, cookie, forms):
        item_id = forms.get('id')
        self._shopdb.remove_item(item_id)
        myuser = cookie[0]
        dcat = cookie[1]
        articles = self._shopdb.get_all_items(dcat);
        flash = {'error':None,
                'notice':'Articolo rimosso correttamente'}
        pdata = {'user':myuser, 'cat':self._shopdb.categories,
                'defcat':dcat, 'articles':articles, 'flash':flash}
        return template('admin/items', tpldata=pdata)

    def remove_category(self, cookie, forms):
        catid = forms.get('id')
        self._shopdb.remove_category(catid)
        flash = {'error':None, 'notice':'Categoria rimossa'}
        pdata = {'user':cookie[0], 'cat':self._shopdb.categories,
                'flash':flash}
        return template('admin/index', tpldata=pdata)

    def modify_category(self, cookie, forms):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        catid = forms.get('id')
        cat_code = forms.get('catcode')
        cat_description = forms.get('description')
        record = (cat_code, cat_description, now, catid)
        self._shopdb.modify_category(record)
        flash = {'error':None,
                'notice':'Categoria modificata correttamente'}
        pdata = {'user':cookie[0], 'cat':self._shopdb.categories,
                'flash':flash}
        return template('admin/index', tpldata=pdata)

    def add_category(self, cookie, forms):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        cat_code = forms.get('catcode')
        cat_description = forms.get('description')
        record = (None, cat_code, cat_description, now, None)
        self._shopdb.add_category(record)
        flash = {'error':None,
                'notice':'Categoria creata correttamente'}
        pdata = {'user':cookie[0], 'cat':self._shopdb.categories,
                'flash':flash}
        return template('admin/index', tpldata=pdata)

    def upload_csv_pricelist(self, myfile):
        self._shopdb.remove_all_items()
        mycat = {}
        n = 0

        # Create a dict
        for key in self._shopdb.categories:
            mycat[key[1]] = key[0]

        reader = csv.reader(myfile.file, delimiter=';')
        # Jump over the 1st description's line.
        reader.next()

        for row in reader:
            n += 1
            price1 = float(string.replace(row[4], ',', '.'))
            price2 = float(string.replace(row[5], ',', '.'))
            code_cat = row[6].strip()
            qta = int(row[3])

            if code_cat in mycat:
                cat_id = mycat[code_cat]
            else:
                # this is a bug and you know it!
                cat_id = None

            this_item = [None, cat_id, code_cat, row[0].strip(),
                    row[1].strip(), row[2].strip(), qta,
                    None, price1, price2]

            self._shopdb.add_item(this_item)

        return (n)

    def upload_csv_promo(self, myfile):
        """
        Load a promo CSV file.

        BUG: code_cat should be the real code_cat from cat_id = 1,
        this can be different from '0'.
        """

        cat_id = 1
        code_cat = '0'
        self._shopdb.remove_all_items(cat_id)
        n = 0
        reader = csv.reader(myfile.file, delimiter=';')
        reader.next()

        for row in reader:
            n += 1
            price1 = float(string.replace(row[4], ',', '.'))
            price2 = float(string.replace(row[5], ',', '.'))
            qta = int(row[3])
            this_item = [None, cat_id, code_cat, row[0].strip(),
                    row[1].strip(), row[2].strip(), qta,
                    None, price1, price2]

            self._shopdb.add_item(this_item)

        return (n)

    def pricelists(self, cookie, flash=None):
        self._config.update_mtime()
        return template('admin/pricelists.tpl', user=cookie[0],
                pricelists=self._config.pricelists, flash=flash)

    def promo(self, cookie, flash=None):
        return template('admin/promo.tpl', user=cookie[0],
                promo=self._config.promo, flash=flash)

if __name__ == "__main__":
    print "Cannot execute as program!"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
