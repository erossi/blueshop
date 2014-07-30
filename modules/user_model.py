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

import os
import time
import hashlib
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session, aliased
from sqlalchemy.ext.declarative import declarative_base

# FIXME Remove me once sqlalchemy works
import sqlite3

# FIXME add memcache support
#import memcache_model

UserBase = declarative_base()
LoginBase = declarative_base()

class Users(UserBase):
    """
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    code = Column(String(length=15, convert_unicode=True),
            nullable = False)
    company = Column(String(length=255, convert_unicode=True),
            nullable = False)
    vat_code = Column(String(length=15, convert_unicode=True),
            nullable = False)
    owner = Column(String(length=255, convert_unicode=True),
            nullable = False)
    email = Column(String(length=255), nullable = False)
    password = Column(String(length=255), nullable = False)
    address = Column(String(length=255, convert_unicode=True),
            nullable = False)
    city = Column(String(length=255, convert_unicode=True),
            nullable = False)
    region = Column(String(length=255, convert_unicode=True),
            nullable = False)
    postal = Column(String(length=255, convert_unicode=True),
            nullable = False)
    country = Column(String(length=255, convert_unicode=True),
            nullable = False)
    phone = Column(String(length=255, convert_unicode=True),
            default=False)
    fax = Column(String(length=255, convert_unicode=True),
            default=False)
    address2 = Column(String(length=255, convert_unicode=True),
            default=False)
    city2 = Column(String(length=255, convert_unicode=True),
            default=False)
    region2 = Column(String(length=255, convert_unicode=True),
            default=False)
    postal2 = Column(String(length=255, convert_unicode=True),
            default=False)
    country2 = Column(String(length=255, convert_unicode=True),
            default=False)
    phone2 = Column(String(length=255, convert_unicode=True),
            default=False)
    fax2 = Column(String(length=255, convert_unicode=True),
            default=False)
    comment = Column(TEXT, default=False)
    email_valid = Column(Boolean, default=True)
    email_pricelist = Column(Boolean, default=True)
    email_promo = Column(Boolean, default=True)
    disabled = Column(Boolean, default=True)
    web_access = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    pricelist = Column(Integer, default=0)
    created = Column(DateTime)
    last_update = Column(DateTime)

    def __init__(self, code, company, vat_code, owner, email, password, \
            address, city, region, postal, country):
        """
        """
        self.code = code
        self.company = company
        self.vat_code = vat_code
        self.owner = owner
        self.email = email
        self.password = password
        self.address = address
        self.city = city
        self.region = region
        self.postal = postal
        self.country = country


class Logins(LoginBase):
    """
    """
    __tablename__ = 'logins'
    loginid = Column(Integer, primary_key=True)
    email = Column(String(length=255, convert_unicode=True),
            nullable = False)
    date = Column(DateTime)

    def __init__(self, email, utctime):
        """
        """
        self.email = email
        self.date = utctime


class UserDb(object):
    """ The user model class (to be removed).

    All the user DB operations pass from here.
    """

    # Db attributes
    _userdb_engine = None
    _logindb_engine = None
    _session_user = None
    _session_login = None
    users = Users
    logins = Logins

    # MemCache obj (to be implemented)
    _mc = None

    # user attributes (to be implemented)
    _user = {}
    _sessid = None
    _sessttl = None
    _debug = False
    # fixed flag level
    _administrator = False

    # Deprecated old sqlite direct attributes.
    _conn = None
    _cur = None
    _config = None

    # Attribute Users present in the db.
    users = {}
    # sane defaults if not specified in the cfg file.
    users['paginate'] = 5

    def _adjust_cursors(self, cursor, total):
        """
        """
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
        """
        """
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

    def __init__(self, config, createdb=False):
        """
        """
        self._debug = config.site['debug']

        if self._debug:
            print "UM config path: ", config.path
#            self._userdb_engine = create_engine('sqlite:///' + \
#                    os.path.join(config.path['db'], config.db['users']),
#                    echo=True, echo_pool=True)
            self._logindb_engine = create_engine('sqlite:///' + \
                    os.path.join(config.path['db'], config.db['logins']),
                    echo=True, echo_pool=True)
        else:
#            self._userdb_engine = create_engine('sqlite:///' + \
#                    os.path.join(config.path['db'], config.db['users']))
            self._logindb_engine = create_engine('sqlite:///' + \
                    os.path.join(config.path['db'], config.db['logins']))

        # Create the db if requested
        if createdb:
#            UserBase.metadata.create_all(self._userdb_engine)
            LoginBase.metadata.create_all(self._logindb_engine)

#        session_factory_users = sessionmaker(bind=self._userdb_engine)
        session_factory_login = sessionmaker(bind=self._logindb_engine)
#        self._session_user = scoped_session(session_factory_users)
        self._session_login = scoped_session(session_factory_login)

        # memcache session should expire later than the cookie.
        if 'session_ttl' in config.users:
            self._sessttl = int(config.users['session_ttl'])
        elif 'cookie_timeout' in config.users:
            self._sessttl = int(config.users['cookie_timeout'])
        else:
            self._sessttl = 300

        # self._mc = memcache_model.MemCache(config, "um_", self._sessttl)

        # Old sqlite direct access to be removed.
        self._config = config
        self.users['paginate'] = int(self._config.users['paginate'])

        self._conn = sqlite3.connect(self._config.db['users'])
        self._cur = self._conn.cursor()
        self._update_attributes()

    def __del__(self):
        """
        """
#        self._session_user.remove()
        self._session_login.remove()
#        self._userdb_engine.dispose()
        self._logindb_engine.dispose()

        # Old sqlite to be removed
        self._conn.close()

    def check_login(self, username, password):
        """ Check username and password """

        self._cur.execute("select id, ragsoc, email, \
                listino, admin from users where email=? and password=? \
                and web_access='t'", (username, password))
        rawuser = self._cur.fetchone()
        myuser = {}

        if rawuser:
            for idx, col in enumerate(self._cur.description):
                myuser[col[0]] = rawuser[idx]

        return (myuser)

    def record_login(self, username):
        """ Record the login in the logins database.
        """
        self._session_login.add(Logins(username, datetime.utcnow()))
        self._session_login.commit()

    def recover_password(self, email, piva):
        self._cur.execute("select email, password from users where \
                email=? or piva=?", (email, piva))
        return (self._cur.fetchone())

    def _get_last_logins(self, email):
        """ Get the last 3 logins for the user.

        select created_at from logins where user_id=email \
                order by created_at DESC LIMIT 3;
        """
        query = self._session_login.query(Logins.date)
        query = query.filter(Logins.email == email)
        query = query.order_by(Logins.date.desc())
        query = query.limit(3)
        return(query.all())

    def get_all_infos(self, uid):
        self._cur.execute("select * from users where id = ?", (uid,))
        rawuser = self._cur.fetchone()
        myuser = {}

        if rawuser:
            for idx, col in enumerate(self._cur.description):
                myuser[col[0]] = rawuser[idx]

            myuser['logins'] = self._get_last_logins(myuser['email'])

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
