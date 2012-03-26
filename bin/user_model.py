#!/usr/bin/env python

import sqlite3
import time

class UserDb:
    """
    The user model class.

    All the user DB operations pass from here.
    """

    _conn = None
    _cur = None
    _config = None

    # Attribute Users present in the db.
    users = {}
    users['paginate'] = 5

    def _adjust_cursors(self, cursor, total):
        self.users['first'] = cursor
        self.users['last'] = self.users['first'] + len(self.users['list'])
        self.users['last'] -= 1 

        self.users['prev'] = cursor - self.users['paginate']
        self.users['next'] = cursor + self.users['paginate']

        if self.users['prev'] < 0:
            self.users['prev'] = 0

        if self.users['next'] >= total:
            self.users['next'] = 0

    def _update_attributes(self):
        self._cur.execute("select count(*) from users")
        self.users['total'] = self._cur.fetchone()[0]

        self._cur.execute("select count(*) from users where listino = 1")
        self.users['price1'] = self._cur.fetchone()[0]

        self._cur.execute("select count(*) from users where listino = 2")
        self.users['price2'] = self._cur.fetchone()[0]

        self._cur.execute("select count(*) from users where listino = 3")
        self.users['price3'] = self._cur.fetchone()[0]

        self._cur.execute("select count(*) from users where listino = 4")
        self.users['price4'] = self._cur.fetchone()[0]

        self._cur.execute("select count(*) from users \
                where email_valid = 't'")
        self.users['email'] = self._cur.fetchone()[0]

        self._cur.execute("select count(*) from users \
                where web_access = 't'")
        self.users['www'] = self._cur.fetchone()[0]

        self._cur.execute("select count(*) from users \
                where email_promo = 't'")
        self.users['promo'] = self._cur.fetchone()[0]

    def __init__(self, config):
        self._config = config
        self._conn = sqlite3.connect(self._config.db['users'])
        self._cur = self._conn.cursor()
        self._update_attributes()

    def __del__(self):
        self._conn.close()

    def check_login(self, username, password):
        """ Check username and password """

        self._cur.execute("select id, ragsoc, email, \
                listino, admin from users where email=? and password=? \
                and status='a'", (username, password))
        rawuser = self._cur.fetchone()
        myuser = {}

        if rawuser:
            for idx, col in enumerate(self._cur.description):
                myuser[col[0]] = rawuser[idx]

        return (myuser)

    def record_login(self, record):
        self._cur.execute("insert into logins values (?,?,?,?)", record)
        self._conn.commit()

    def recover_password(self, email, piva):
        self._cur.execute("select email, password from users where \
                email=? or piva=?", (email, piva))
        return (self._cur.fetchone())

    def get_all_infos(self, uid):
        self._cur.execute("select * from users where id = ?", (uid,))
        rawuser = self._cur.fetchone()
        myuser = {}

        if rawuser:
            for idx, col in enumerate(self._cur.description):
                myuser[col[0]] = rawuser[idx]

        return (myuser)

    def exist(self, email, piva):
        self._cur.execute("select count(*) from users where \
                email = ? or piva = ?",
                (email, piva))
        if self._cur.fetchone()[0]:
            return (True)
        else:
            return (False)
        
    def add(self, record):
        self._cur.execute("insert into users values (\
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                ?,?,?,?,?,?,?,?,?,?,?,?,?)", record)
        self._conn.commit()
        self._update_attributes()

    def delete(self, uid):
        self._cur.execute("delete from users where id=?", (uid,))
        self._conn.commit()
        self._update_attributes()

    def modify(self, myuser, uid):
        """
        Change the user field.

        note: uid is taken from the cookie and not from
        the eventually forged post-form infos.
        """
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        query_str = 'update users set '
        mylist = []

        for key in myuser:
            query_str += "'" + key + "'=?,"
            mylist.append(myuser[key])

        # add updated_at field
        query_str += "'updated_at'='" + now + "' where id=" + str(uid)
        self._cur.execute(query_str, mylist)
        self._conn.commit()

    def list(self, cursor=0):
        if cursor < self.users['total']:
            query = "select id, \
                piva, ragsoc, email, email_valid, email_listino, \
                email_promo, web_access, listino from users "
            query += "order by ragsoc limit ? offset ?"
            self._cur.execute(query, (self.users['paginate'], cursor))
            self.users['list'] = self._cur.fetchall()

        self._adjust_cursors(cursor, self.users['total'])

    def list_search(self, cursor=0, search=None):
        search = '%' + search + '%'
        query = "select count(*) from users"
        queryc = " where email like ? or ragsoc like ?"
        queryo = " order by ragsoc limit ? offset ?"
        query += queryc
        self._cur.execute(query, (search, search))
        total = self._cur.fetchone()[0]

        if cursor < total:
            query = "select id, \
                piva, ragsoc, email, email_valid, email_listino, \
                email_promo, web_access, listino from users"
            query += queryc + queryo
            self._cur.execute(query, (search, search,
                    self.users['paginate'], cursor))
            self.users['list'] = self._cur.fetchall()

        self._adjust_cursors(cursor, total)
        return (total)

    def find_email_pricelist(self, pricelist):
        query = "select email from users where \
                email_valid='t' and email_listino='t' and listino=? \
                order by ragsoc"
        self._cur.execute(query, (pricelist,))
        return (self._cur.fetchall())

    def find_email_promo(self):
        query = "select email from users where \
                email_valid='t' and email_promo='t' \
                order by ragsoc"
        self._cur.execute(query)
        return (self._cur.fetchall())


if __name__ == "__main__":
    print "Cannot execute as program!"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
