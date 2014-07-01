#!/usr/bin/env python

import sqlite3
import time

class ShopDb:
    """A simple example class"""

    _conn = None
    _cur = None
    _config = None

    # categories is a list of tuples as:
    # [(cat_id, u'id', u'description', u'created at', u'updated at'),]
    categories = None

    def _get_all_categories(self):
        self._cur.execute("select * from categories")
        self.categories = self._cur.fetchall()

    def __init__(self, config):
        self._config = config
        self._conn = sqlite3.connect(self._config.db['shop'])
        self._cur = self._conn.cursor()
        self._get_all_categories()

    def __del__(self):
        self._conn.close()

    def _max_qta(self, catcode, qta):
        """
        Return the max quantity to show as available for a
        given category.
        """
        # List which categories should be cut off.
        q10 = (36,)
        q30 = (11, 13, 18, 22)
        q1000 = (16,)

        if (catcode in q10) and (qta > 10):
            qta = 10
        elif (catcode in q30) and (qta > 30):
            qta = 30
        elif (catcode in q1000) and (qta > 1000):
            qta = 1000
        else:
            if qta > 100:
                qta = 100

        return (qta)

    def _item_image_filename(self, item):
        """ Get the filename of a given itemcode. """

        if not item[13]:
            filename = '/categories/' + item[2] + '.png'
            # add the new element to the list.
            item = item[:13] + (filename,) + item[14:]

        return (item)

    def get_item(self, item_id):
        self._cur.execute("select * from articles where id=?", (item_id,))
        item = self._cur.fetchone()
        item = self._item_image_filename(item)
        return (item)

    def get_all_items(self, catid):
        self._cur.execute("select * from articles where category_id=?", (catid,))
        rawitems = self._cur.fetchall()
        items = {}
        
        # Json-ize the result as {item_id : [idem_id, ]}
        for record in rawitems:
            record = self._item_image_filename(record)
            items[record[0]] = record

        return (items)
        
    def get_all_cart_items(self, mycart, user_price_list):
        # the fullcart is:
        # {itemId: [IdemCode, 'description', 'description2', price, qta]}
        myshoppingcart = {}

        for itemid in mycart:
            self._cur.execute("select id, codice_art, descrizione, \
                    descrizione2, price, price1, price2, price3, price4 \
                    from articles where id=?", (itemid,))
            rawitem = self._cur.fetchone()
            myitem = {}

            # Prepare the price for this item
            if rawitem:
                myitem['id'] = rawitem[0]
                myitem['itemcode'] = rawitem[1]
                myitem['desc'] = rawitem[2]
                myitem['desc2'] = rawitem[3]
                myitem['price'] = rawitem[4 + user_price_list]
                myshoppingcart[itemid] = myitem

        return (myshoppingcart)

    def remove_item(self, item_id):
        self._cur.execute("delete from articles where id=?", (item_id,))
        self._conn.commit()

    def add_item(self, item):
        """
        Add an item to the database.
        
        First adjust the maximum quatity for the item.
        """

        item[6] = self._max_qta(item[2], item[6])
        self._cur.execute("insert into articles values \
                (?,?,?,?,?,?,?,?,?,?,NULL,NULL,NULL,NULL,NULL,\
                NULL,NULL,NULL,NULL,NULL)", item)
        self._conn.commit()

    def remove_all_items(self, catid=None):
        """
        Remove all items from the database or a category.

        If catid is None then all items are removed from the
        database, else only the items of the category id will be
        removed.
        """

        if not catid:
            self._cur.execute("delete from articles")
        else:
            self._cur.execute("delete from articles where category_id = ?",
                    (catid,))

        self._conn.commit()

    def remove_category(self, catid):
        self._cur.execute("delete from articles where category_id=?", (catid,))
        self._cur.execute("delete from categories where id=?", (catid,))
        self._conn.commit()
        # refresh the categories
        self._get_all_categories()

    def modify_category(self, category):
        self._cur.execute("update categories set codice_cat=?, \
                descrizione=?, updated_at=? where id=?", category)
        self._conn.commit()
        # refresh the categories
        self._get_all_categories()

    def add_category(self, category):
        self._cur.execute("insert into categories values (?,?,?,?,?)",
                category)
        self._conn.commit()
        # refresh the categories
        self._get_all_categories()

if __name__ == "__main__":
    print "Cannot execute as program!"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
