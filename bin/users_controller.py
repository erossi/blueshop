#!/usr/bin/env python

import time
from bottle import request, response, template

# the cookie is in the form of:
# [{'id': int, 'ragsoc': u'text', 'email': u'@text', 'listino': int,
#   'admin': 't | f'}, int]

class User:
    """
    The users controller.
    """

    _secret = 'changeme'
    _mail = None
    _config = None

    # The db object
    _db = None


    def __init__(self, db, mail, config):
        self._mail = mail
        self._db = db
        self._config = config

    def __del__(self):
        pass

    def _random_chars(self, size):
        """
        Generate a random number of chars and number
        of size-lenght
        """

        chars = string.ascii_lowercase + string.digits
        string = ''

        for x in range(size):
            string += random.choice(chars)

        return (string)

    def set_cookie(self, urecord):
        """
        Set the cookie to keep the connection opened.
        The timeout should be configurable in the config file, not
        hardcoded here.
        """

        if urecord:
            response.set_cookie('auth', urecord, max_age=600, path='/', secret=self._secret)
            #response.set_cookie('auth', urecord, path='/', secret=self._secret)
        else:
            # Remove the cookie, logout
            response.set_cookie('auth', None, max_age=1, path='/', secret=self._secret)

    def uid(self, cookie):
        """ Return the user id stored in the cookie """
        return (cookie[0]['id'])

    def is_admin(self, cookie):
        """ Check if the user is an admin user. """

        print "FIXME: Admin check should not relay on cookie"
        if cookie[0]['admin'] == 't':
            return (True)
        else:
            return (False)

    def pricelist(self, cookie):
        """ Return the pricelist of the user """
        return (cookie[0]['listino'])

    def auth(self):
        """ ask for the cookie from the browser """
        cookie = request.get_cookie('auth', secret=self._secret)

        # if we have some cookie refresh the timeout of it
        if cookie:
            self.set_cookie(cookie)

            # if the user is an admin you should not trust
            # the cookie about it and recheck the db.
            if self.is_admin(cookie):
                pass

        # return the info stored in the cookie
        return (cookie)

    def check_login(self, username, password):
        """ Check username and password """

        myuser = self._db.check_login(username, password)

        if myuser:
            # append the default category selected.
            cookie = [myuser, 1]
            self.set_cookie(cookie)
            # record the login date
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            record = (None, myuser['id'], now, None)
            self._db.record_login(record)

        return (myuser)

    def recover_password(self, email, piva):
        myuser = None

        if email or piva:
            myuser = self._db.recover_password(email, piva)

        if myuser:
            # send email to the client
            self._mail.recover_password(myuser)
            return (True)
        else:
            return (False)
        

    def get_all_infos(self, uid):
        myuser = self._db.get_all_infos(uid)
        return (myuser)

    def logout(self):
        self.set_cookie(None)

    def add(self, newuser):
        """ Add a new user to the database """

        # if no record found with the same email, then
        if not self._db.exist(newuser['email'], newuser['piva']):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            record = (None, newuser['piva'],newuser['ragsoc'],
                    newuser['piva'],
                    newuser['respcom'],newuser['email'],
                    'f', # email_valid
                    newuser['email_listino'],
                    newuser['sede_via'],
                    newuser['sede_civico'], newuser['sede_citta'],
                    newuser['sede_prov'], newuser['sede_cap'],
                    newuser['sede_tel'], newuser['sede_fax'],
                    newuser['sede_stato'],
                    newuser['sede_via_2'],
                    newuser['sede_civico_2'], newuser['sede_citta_2'],
                    newuser['sede_prov_2'], newuser['sede_cap_2'],
                    newuser['sede_tel_2'], newuser['sede_fax_2'],
                    newuser['sede_stato_2'],
                    newuser['attivita'],
                    'r', # status
                    'f', # web_access
                    't', # email_promo
                    newuser['password'],
                    1, # listino
                    'f', # admin
                    now,now)

            self._db.add(record)
            # send mail to confirm the registration.
            print "FIXME: Require re-captcha and 2 phase registration"
            self._mail.add_user(newuser)
        else:
            newuser['error'] = "Errore: Questa email o P.IVA e' gia' \
                    presente nell'archivio."

        return (newuser)

    def modify(self, myuser, uid):
        self._db.modify(myuser, uid)

    def list(self, cookie, cursor=0, search=None, flash=None):
        myuser = cookie[0]

        if search:
            total = self._db.list_search(cursor, search)
            flash = {}
            flash['notice'] = str(total) + " risultati trovati."
            flash['error'] = None
        else:
            self._db.list(cursor)

        return template('admin/users', user=myuser, allusers=self._db.users,
                cursor=cursor, search=search, flash=flash)

    def delete(self, cookie, uid=None):
        """
        Remove a user from the database.

        When uid is None then a normal user try to remove himself
        from the modify user menu.

        bug: should prevent an admin user to remove himself from
        the remove user admin menu without logging out and remove
        the cookie.
        """

        myuser = cookie[0]

        if uid is None:
            uid = cookie[0]['id']

        self._db.delete(uid)
        flash = {'error':None, 'notice':'Utente rimosso!'}
        self._db.list()

        return template('admin/users', user=myuser, allusers=self._db.users,
                cursor=0, search=None, flash=flash)

    def mail_pricelists(self, cookie, subject, msg):
        # file 1
        file_to_send = self._config.pricelists['file1']
        users_to_send = self._db.find_email_pricelist(1)

        if users_to_send:
            self._mail.pricelists(file_to_send, users_to_send, subject, msg)

        # file 2
        file_to_send = self._config.pricelists['file2']
        users_to_send = self._db.find_email_pricelist(2)

        if users_to_send:
            self._mail.pricelists(file_to_send, users_to_send, subject, msg)

        # file 3
        file_to_send = self._config.pricelists['file3']
        users_to_send = self._db.find_email_pricelist(3)

        if users_to_send:
            self._mail.pricelists(file_to_send, users_to_send, subject, msg)

    def mail_promo(self, cookie, subject, msg):
        users_to_send = self._db.find_email_promo()

        if users_to_send:
            self._mail.promo(users_to_send, subject, msg)

if __name__ == "__main__":
    print "Cannot execute as program!"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
