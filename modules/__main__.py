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

""" BlueShop python release.
"""

__author__ = "Enrico Rossi <e.rossi@tecnobrain.com>"
__credits__ = """ Blue Tech Informatica s.r.l. """

import os
import sys
import bottle

# Please patch this to fit your installation.
# Configuration file path
if os.getenv('BLUESHOP_PATH'):
    modules_path = os.getenv('BLUESHOP_PATH')
else:
    modules_path = '/opt/blueshop'

sys.path.insert(0, modules_path)

from modules import _version_, _lastupdate_
from modules import _tagged_version_, _git_version_
from modules import config
from modules import admin_controller
from modules import parser_controller
from modules import user_controller
from modules import shop_controller
from modules import shop_model

__version__ = _version_
__last_update__ = _lastupdate_

# object definition
config = config.Config()
shopdb = shop_model.ShopDb(config)
user = user_controller.User(config)
shop = shop_controller.Shop(shopdb, config)
admin = admin_controller.Admin(shopdb, config)
fieldparser = parser_controller.FieldParser()

# Set the _debug vars. and the bottle debug env.
_debug = config.site['debug']

if _debug:
    print 'DEBUG enabled.'
    bottle.debug(True)

# Define template path
template_path = os.path.join(config.path['base'], 'views')
overlay_path = os.path.join(config.path['overlay'], 'views')
bottle.TEMPLATE_PATH.insert(0, template_path)
bottle.TEMPLATE_PATH.insert(0, overlay_path)

#
# Local functions
#

def _auth():
    """ Authenticate normal users """

    cookie = user.auth()

    if cookie:
        shop.chart_new(cookie[0]['id'])

    return (cookie)

def _admin_auth():
    """ Authenticate admin users """

    cookie = _auth()

    if cookie and (cookie[0]['admin'] == 't'):
        return (cookie)
    else:
        return (None)

# Decorators
def auth(fn):
    def wrapper():
        cookie = _auth()

        if cookie:
            tplpage = fn(cookie)
        else:
            tplpage = bottle.redirect('/')

        return (tplpage)
    return wrapper

# Create the bottle object
# Called application for wsgi compatibility
application = bottle.Bottle()

#
# Main route
#

@application.route('/')
def callback():
    cookie = _auth()

    if cookie:
        if user.is_admin(cookie):
            tplpage = bottle.redirect('/admin/index')
        else:
            tplpage = bottle.redirect('/shop/index')
    else:
        tplpage = bottle.template('user/login', error=None)

    return (tplpage)

@application.route('/main/contacts')
def callback():
    """
    """
    return (bottle.template('main/contacts'))

@application.route('/main/about')
def callback():
    """
    """
    return(bottle.template('main/about'))

@application.route('/main/recover_password', method='get')
def callback():
    return(bottle.template('main/recover_password', flash=None))

@application.route('/main/recover_password', method='post')
def callback():
    """
    """
    email = bottle.request.forms.get('email')
    piva = bottle.request.forms.get('piva')
    # check email address and piva agains sql injection
    print "FIXME: parse against sql injection"

    if user.recover_password(email, piva):
        flash = {'error':None, 'notice':"Email spedita con successo"}
    else:
        flash = {'error':"Non esiste un record corrispondente",
                'notice':None}

    return(bottle.template('main/recover_password', flash=flash))

#
# Admin route
#

@application.route('/admin/index', method='get')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        myuser = cookie[0]
        pdata = {'user':myuser, 'cat':shopdb.categories, 'flash':None}
        tplpage = bottle.template('admin/index', tpldata=pdata)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/index', method='post')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        if bottle.request.forms.get('commit') == 'X':
            tplpage = admin.remove_category(cookie, bottle.request.forms)

        elif bottle.request.forms.get('commit') == 'Modifica':
            tplpage = admin.modify_category(cookie, bottle.request.forms)

        elif bottle.request.forms.get('commit') == 'Aggiungi':
            tplpage = admin.add_category(cookie, bottle.request.forms)

        else:
            tplpage = "Shouldn't appened!"
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/items', method='get')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        tplpage = admin.items(cookie)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/items', method='post')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        if bottle.request.forms.get('whichform') == 'rmitem':
            tplpage = admin.item_remove(cookie, bottle.request.forms)

        elif bottle.request.forms.get('whichform') == 'chcat':
            cookie[1] = int(bottle.request.forms.get('codcat'))
            print "FIXME: default category not stored in the cookie"
            tplpage = admin.items(cookie)
        else:
            tplpage = "This Shouldn't appened!"
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/upload_csv_pricelist', method='post')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        myfile = bottle.request.files.filedata

        if myfile.filename == "listino.csv":
            # nuke the carts
            shop.remove_all_carts()
            num = admin.upload_csv_pricelist(myfile)
            flash = {'error':None}
            flash['notice'] = "Caricati {0:d} articoli".format(num)
            tplpage = admin.items(cookie, flash)
        else:
            tplpage = "Shit wrong filename."

    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/upload_csv_promo', method='post')
def callback():
    """ Upload the promo csv file.

    bug: void all carts is a bug, should remove only the existing
    promo's item eventually present in the carts.
    """
    cookie = _admin_auth()

    if cookie:
        myfile = bottle.request.files.filedata

        if myfile.filename == "promo.csv":
            # nuke the carts
            shop.remove_all_carts()
            num = admin.upload_csv_promo(myfile)
            flash = {'error':None}
            flash['notice'] = "Caricati {0:d} articoli".format(num)
            tplpage = admin.items(cookie, flash)
        else:
            tplpage = "Shit wrong filename."

    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/upload_pricelist', method='post')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        myfile = bottle.request.files.filedata

        if myfile.filename == config.pricelists['filename1']:
            filename = config.pricelists['file1']
        elif myfile.filename == config.pricelists['filename2']:
            filename = config.pricelists['file2']
        elif myfile.filename == config.pricelists['filename3']:
            filename = config.pricelists['file3']
        else:
            filename = None
            flash = {'error':'File NON accettato', 'notice':None}

        if filename:
            outfile = open(filename, 'w')
            outfile.write(myfile.file.read())
            outfile.close()
            flash = {'error':None, 'notice':"Caricato"}

        tplpage = admin.pricelists(cookie, flash)

    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/users', method='get')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        tplpage = user.list(cookie)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/users', method='post')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        search = bottle.request.forms.get('search')

        if search == "None":
            search = None

        if "next" in bottle.request.forms.get('commit'):
            cursor = int(bottle.request.forms.get('cursornext'))
        elif "prev" in bottle.request.forms.get('commit'):
            cursor = int(bottle.request.forms.get('cursorprev'))
        elif "Cerca" in bottle.request.forms.get('commit'):
            cursor = 0
        else:
            search = None

        tplpage = user.list(cookie, cursor, search)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/changeuser', method='get')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        uid = bottle.request.query.id
        user_info = user.get_all_infos(uid)
        tplpage = bottle.template('admin/chuser', tpldata=user_info,
            user=cookie[0], flash=None)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/changeuser', method='post')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        flash = {}
        uid = bottle.request.forms.get('uid')
        user_info = user.get_all_infos(uid)

        # patch against missini password confirmation
        bottle.request.forms.append('password_confirmation',
                bottle.request.forms.get('password'))

        # check for the consistency of all field
        # return only those field to be updated
        newuser = fieldparser.user_modify(user_info, bottle.request.forms)

        # and if there isn't any error
        if newuser['error'] is None:
            flash['error'] = None
            # purge error key from newuser
            del(newuser['error'])

            if len(newuser):
                user.modify(newuser, user_info['id'])
                user_info = user.get_all_infos(uid)
                flash['notice'] = 'Registrazione aggiornata.'
            else:
                flash['notice'] = 'Nessuna modifica effettuata.'

        else:
            flash['error'] = newuser['error']
            flash['notice'] = None

        tplpage = bottle.template('admin/chuser', tpldata=user_info,
            user=cookie[0], flash=flash)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/rmuser', method='get')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        uid = bottle.request.query.id
        tplpage = user.delete(cookie, uid)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/pricelists', method='get')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        tplpage = admin.pricelists(cookie)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/pricelists', method='post')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        subject = bottle.request.forms.get('subject')
        msg = bottle.request.forms.get('message')
        user.mail_pricelists(cookie, subject, msg)
        flash = {'error':None, 'notice':'Spediti listini via email'}
        tplpage = admin.pricelists(cookie, flash)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/download_pricelist', method='get')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        pricelist = int(bottle.request.query.pl)
        filename = shop.download_pricelist(pricelist)

        if filename:
            return(bottle.static_file(filename, \
                    root=config.path['private'], \
                    download=filename, \
                    mimetype=config.pricelists['mimetype']))

@application.route('/admin/promo', method='get')
def callback():
    """

    bug: bottle.redirect() is an exceptions
    """
    cookie = _admin_auth()

    if cookie:
        tplpage = admin.promo(cookie)
    else:
        # BUG, this is an exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/admin/promo', method='post')
def callback():
    """
    """
    cookie = _admin_auth()

    if cookie:
        subject = bottle.request.forms.get('subject')
        msg = bottle.request.forms.get('message')
        user.mail_promo(cookie, subject, msg)
        flash = {'error':None, 'notice':'Spedite promo via email'}
        tplpage = admin.promo(cookie, flash)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

#
# User route
#

@application.route('/user/login', method='get')
def callback():
    """
    """
    return(bottle.template('user/login', error=None))

@application.route('/user/login', method='post')
def callback():
    """

    bug: exception.
    """
    email = bottle.request.forms.get('email')
    password = bottle.request.forms.get('password')
    # parse the input field
    email = fieldparser.email(email)
    password = fieldparser.password(password)

    if user.check_login(email, password):
        print "FIXME: login void the chart?"
        # FIXME exception!
        return(bottle.redirect('/shop/index'))
    else:
        return(bottle.template('user/login', error="Login failed!"))

@application.route('/user/add', method='get')
def callback():
    """
    """
    tpldata = fieldparser.user_add(None)
    return(bottle.template('user/add', tpldata=tpldata))

@application.route('/user/add', method='post')
def callback():
    """ Add a new user
    """

    # check for the consistency of all field
    newuser = fieldparser.user_add(bottle.request.forms)

    if newuser['error'] is None:
        newuser = user.add(newuser)

        if newuser['error'] is None:
            newuser = fieldparser.user_add(None)
            newuser['notice'] = 'Registrazione inviata correttamente.'

    return(bottle.template('user/add', tpldata=newuser))

@application.route('/user/modify', method='get')
@auth
def callback(cookie):
    """
    """
    uid = user.uid(cookie)
    user_info = user.get_all_infos(uid)
    # add error and notice
    user_info['flash'] = None
    return(bottle.template('user/modify', tpldata=user_info))

@application.route('/user/modify', method='post')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        flash = {'error':None, 'notice':None}
        uid = user.uid(cookie)
        user_info = user.get_all_infos(uid)
        # check for the consistency of all field
        # return only those field to be updated
        newuser = fieldparser.user_modify(user_info, bottle.request.forms)

        # and if there isn't any error
        if newuser['error'] is None:
            # purge error key from newuser
            del(newuser['error'])

            if len(newuser):
                user.modify(newuser, user_info['id'])
                user_info = user.get_all_infos(uid)
                flash['notice'] = 'Registrazione aggiornata.'
            else:
                flash['notice'] = 'Nessuna modifica effettuata.'
        else:
            flash['error'] = newuser['error']

        user_info['flash'] = flash
        tplpage = bottle.template('user/modify', tpldata=user_info)
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/user/rmuser', method='get')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        user.delete(cookie)

    # Remove the cookie
    user.logout()
    # FIXME exception
    return(bottle.redirect('/'))

@application.route('/user/logout')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        shop.chart_del(user.uid(cookie))

    # Remove the cookie
    user.logout()
    # FIXME exception
    return(bottle.redirect('/'))

#
# Shop route
#

@application.route('/shop/index', method='get')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        tplpage = shop.index(cookie)
    else:
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/shop/index', method='post')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        cookie[1] = int(bottle.request.forms.get('codcat'))
        print "FIXME: default category not stored in the cookie"
        tplpage = shop.index(cookie)
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/shop/buy')
def callback():
    """
    """
    # check if it is an ajax request
    if bottle.request.is_ajax:
        cookie = _auth()

        if cookie:
            # item id and quantity are a GET request.
            item_id = int(bottle.request.query.aid)
            item_qta = int(bottle.request.query.qta)
            uid = user.uid(cookie)
            shop.buy_item(uid, item_id, item_qta)
            return('OK')
        else:
            return('Oops!') # redirect to somewhere

@application.route('/shop/show')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        # is a GET request
        item_id = int(bottle.request.query.aid)
        tplpage = shop.show_item(cookie, item_id)
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/shop/cart', method='get')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        uid = user.uid(cookie)
        # get all infos about this uid from the dbase
        userinfo = user.get_all_infos(uid)
        tplpage = shop.shoppingcart(userinfo)
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/shop/cart', method='post')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        item_id = int(bottle.request.forms.get('aid'))
        uid = user.uid(cookie)
        shop.buy_item(uid, item_id, 0)
        # get all infos about this uid from the dbase
        userinfo = user.get_all_infos(uid)
        tplpage = shop.shoppingcart(userinfo)
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/shop/checkout', method='post')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        uid = user.uid(cookie)
        user_info = user.get_all_infos(uid)
        # add the order information into the user dict.
        user_info['orderinfo'] = bottle.request.forms.get('info')
        chart = shop.checkout(user_info)

        if user.checkout(chart):
            shop.chart_del(user_info['id'])
            flash['notice'] = 'Ordine completato con successo.'
        else:
            flash['error'] = 'Ci sono stati errori di sperizione'

        tplpage = template('store/shoppingcart', tpldata=chart)
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/shop/download_pricelist')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        filename = shop.download_pricelist(user.pricelist(cookie))

        if filename:
            return(bottle.static_file(filename, \
                    root=config.path['private'], \
                    download=config.pricelists['filename'], \
                    mimetype=config.pricelists['mimetype']))

@application.route('/shop/support')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        tplpage = bottle.template('store/support', tpldata=cookie[0])
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/shop/info')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        tplpage = bottle.template('store/info', tpldata=cookie[0])
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

@application.route('/shop/contacts')
def callback():
    """
    """
    cookie = _auth()

    if cookie:
        tplpage = bottle.template('store/contacts', tpldata=cookie[0])
    else:
        # FIXME exception
        tplpage = bottle.redirect('/')

    return(tplpage)

# Images route
@application.route('/images/<filename:re:.*\.png>')
def callback(filename):
    """
    """
    basepath = os.path.join(config.path['base'], 'images')
    mypath = os.path.join(config.path['overlay'], 'images')

    if os.path.isfile(os.path.join(mypath, filename)):
        return(bottle.static_file(filename, \
                root=mypath, mimetype='image/png'))
    else:
        return(bottle.static_file(filename, \
                root=basepath, mimetype='image/png'))


# Static pages and files to be served.
@application.route('/static/<filename:path>')
def callback(filename):
    """
    """
    basepath = os.path.join(config.path['base'], 'static')
    mypath = os.path.join(config.path['overlay'], 'static')

    if os.path.isfile(os.path.join(mypath, filename)):
        return(bottle.static_file(filename, root=mypath))
    else:
        return(bottle.static_file(filename, root=basepath))

#
# Errors
#
#@application.error(401)
#def callback(error):
#    """ UnAuthorized
#    """
#    # before_request()
#
#    if user.auth():
#        tplobj.login=True
#
#    # set the BC
#    tplobj.set_breadcrumbs(title = tplobj.gettext('Error 401'))
#
#    if _debug:
#        print 'Main ERROR 401'
#
#    return(bottle.template('e401', tplobj=tplobj))
#
#@application.error(404)
#def callback(error):
#    """ File Not Found
#    """
#    # before_request()
#
#    if user.auth():
#        tplobj.login=True
#
#    # set the BC
#    tplobj.set_breadcrumbs(title = tplobj.gettext('Error 404'))
#
#    if _debug:
#        print 'Main ERROR 404'
#
#    return(bottle.template('e404', tplobj=tplobj))


#
# Main, internal webserver used for test only.
#
if __name__ == "__main__":
    bottle.run(application, host=config.site['host'], \
            port=config.site['port'])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
