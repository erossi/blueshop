#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2012, 2014 Enrico Rossi
# This file is part of Blueshop.
#
# Blueshop is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Blueshop is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Blueshop. If not, see <http://www.gnu.org/licenses/>.

import sqlite3
import time
from bottle import template

class Shop:
    """A simple example class"""

    _secret = 'changeme'

    # the shopping carts is a tuple composed by uid as a key and
    # the items
    # where the items are themselves a tuple composed by itemCode and qta.
    # shoppingcarts: {UserID: {itemCode: 'quantity'}}
    charts = None

    # The db model
    _shopdb = None

    # the config object
    _config = None

    def __init__(self, db, config):
        self._shopdb = db
        self._config = config
        self.charts = {0: {0: 'placeholder'}}

    def __del__(self):
        pass

    def chart_new(self, uid):
        if uid in self.charts:
            # refresh the time
            self.charts[uid][0] = time.asctime()
        else:
            self.charts[uid]={0: time.asctime()}

        return (self.charts[uid])

    def chart_del(self, uid):
        """ Empty the chart of a user """

        if uid in self.charts:
            del(self.charts[uid])

    def remove_all_carts(self):
        self.charts = {0: {0: 'placeholder'}}

    def index(self, cookie):
        myuser = cookie[0]
        dcat = cookie[1]
        # Create or renew the cart for this user
        mychart = self.charts[myuser['id']]
        articles = self._shopdb.get_all_items(dcat);
        pdata = {'user':myuser, 'cat':self._shopdb.categories,
                'defcat':dcat, 'mychart':mychart, 'articles':articles,
                'flash':None}
        return template('store/index', tpldata=pdata)

    def show_item(self, cookie, item_id):
        myuser = cookie[0]
        dcat = cookie[1]
        # Create or renew the cart for this user
        mychart = self.charts[myuser['id']]
        item = self._shopdb.get_item(item_id);
        pdata = {'user':myuser, 'cat':self._shopdb.categories,
                'defcat':dcat, 'mychart':mychart, 'item':item,
                'flash':None}
        return template('store/item', tpldata=pdata)

    def buy_item(self, uid, aid, qta):
        if qta:
            self.charts[uid][aid] = qta
        else:
            if aid in self.charts[uid]:
                del(self.charts[uid][aid])

    def shoppingcart(self, userinfo):
        mycart = self.charts[userinfo['id']]
        items = self._shopdb.get_all_cart_items(mycart, userinfo['listino']);
        pdata = {'user':userinfo, 'mycart':mycart, 'items':items,
                'flash':None}
        return template('store/shoppingcart', tpldata=pdata)

    def checkout(self, userinfo):
        """
        """
        flash = {'error':None, 'notice':None}
        mycart = self.charts[userinfo['id']]
        items = self._shopdb.get_all_cart_items(mycart, \
                userinfo['listino']);
        return({'user':userinfo, 'mycart':mycart, 'items':items})

    def download_pricelist(self, pricelist):
        if pricelist == 1:
            filename = self._config.pricelists['filename1']
        elif pricelist == 2:
            filename = self._config.pricelists['filename2']
        elif pricelist == 3:
            filename = self._config.pricelists['filename3']
        else:
            filename = None

        return (filename)

if __name__ == "__main__":
    print "Cannot execute as program!"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
