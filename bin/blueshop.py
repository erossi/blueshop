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

"""
bluEShop python release.
"""

__author__ = "Enrico Rossi <e.rossi@tecnobrain.com>"
__date__ = "20 Feb 2012"
__version__ = "$Revision: 0.1b $"
__credits__ = """ Blue Tech Informatica s.r.l. """

import os
from bottle import Bottle
from bottle import route, run, template, get, post, request, response
from bottle import redirect, static_file, debug
import shop_model
import user_model
import users_controller
import shop_controller
import admin_controller
import parser_controller
import mail_controller
import config

# object definition
config = config.Config()
shopdb = shop_model.ShopDb(config)
userdb = user_model.UserDb(config)
mail = mail_controller.MailUtils(config)
user = users_controller.User(userdb, mail, config)
shop = shop_controller.Shop(shopdb, mail, config)
admin = admin_controller.Admin(shopdb, config)
fieldparser = parser_controller.FieldParser()

debug(True)

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

    if cookie[0]['admin'] == 't':
        return (cookie)
    else:
        return (None)

#
# Create the bottle object
#

app = Bottle()

#
# Main route
#

@app.route('/')
def index():
    cookie = _auth()

    if cookie:
        if user.is_admin(cookie):
            tplpage = redirect('/admin/index')
        else:
            tplpage = redirect('/shop/index')
    else:
        tplpage = template('user/login', error=None)

    return (tplpage)

@app.route('/main/contacts')
def main_contacts():
    return template('main/contacts')

@app.route('/main/recover_password', method='get')
def recover_password():
    return template('main/recover_password', flash=None)

@app.route('/main/recover_password', method='post')
def recover_password_submit():
    email = request.forms.get('email')
    piva = request.forms.get('piva')
    # check email address and piva agains sql injection
    print "FIXME: parse against sql injection"

    if user.recover_password(email, piva):
        flash = {'error':None, 'notice':"Email spedita con successo"}
    else:
        flash = {'error':"Non esiste un record corrispondente",
                'notice':None}

    return template('main/recover_password', flash=flash)

#
# Admin route
#

@app.route('/admin/index', method='get')
def adm_index():
    cookie = _admin_auth()

    if cookie:
        myuser = cookie[0]
        pdata = {'user':myuser, 'cat':shopdb.categories, 'flash':None}
        tplpage = template('admin/index', tpldata=pdata)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/index', method='post')
def adm_index_post():
    cookie = _admin_auth()

    if cookie:
        if request.forms.get('commit') == 'X':
            tplpage = admin.remove_category(cookie, request.forms)

        elif request.forms.get('commit') == 'Modifica':
            tplpage = admin.modify_category(cookie, request.forms)

        elif request.forms.get('commit') == 'Aggiungi':
            tplpage = admin.add_category(cookie, request.forms)

        else:
            tplpage = "Shouldn't appened!"
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/items', method='get')
def adm_items():
    cookie = _admin_auth()

    if cookie:
        tplpage = admin.items(cookie)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/items', method='post')
def adm_items_post():
    cookie = _admin_auth()

    if cookie:
        if request.forms.get('whichform') == 'rmitem':
            tplpage = admin.item_remove(cookie, request.forms)

        elif request.forms.get('whichform') == 'chcat':
            cookie[1] = int(request.forms.get('codcat'))
            print "FIXME: default category not stored in the cookie"
            tplpage = admin.items(cookie)
        else:
            tplpage = "This Shouldn't appened!"
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/upload_csv_pricelist', method='post')
def adm_upload_csv_pricelist():
    cookie = _admin_auth()

    if cookie:
        myfile = request.files.filedata

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
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/upload_csv_promo', method='post')
def adm_upload_csv_promo():
    """
    Upload the promo csv file.

    bug: void all carts is a bug, should remove only the existing
    promo's item eventually present in the carts.
    """
    cookie = _admin_auth()

    if cookie:
        myfile = request.files.filedata

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
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/upload_pricelist', method='post')
def adm_upl_pricelists():
    cookie = _admin_auth()

    if cookie:
        myfile = request.files.filedata

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
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/users', method='get')
def adm_users():
    cookie = _admin_auth()

    if cookie:
        tplpage = user.list(cookie)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/users', method='post')
def adm_users():
    cookie = _admin_auth()

    if cookie:
        search = request.forms.get('search')

        if search == "None":
            search = None

        if "next" in request.forms.get('commit'):
            cursor = int(request.forms.get('cursornext'))
        elif "prev" in request.forms.get('commit'):
            cursor = int(request.forms.get('cursorprev'))
        elif "Cerca" in request.forms.get('commit'):
            cursor = 0
        else:
            search = None

        tplpage = user.list(cookie, cursor, search)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/changeuser', method='get')
def adm_chuser():
    cookie = _admin_auth()

    if cookie:
        uid = request.query.id
        user_info = user.get_all_infos(uid)
        tplpage = template('admin/chuser', tpldata=user_info,
            user=cookie[0], flash=None)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/changeuser', method='post')
def adm_chuser():
    cookie = _admin_auth()

    if cookie:
        flash = {}
        uid = request.forms.get('uid')
        user_info = user.get_all_infos(uid)

        # patch against missini password confirmation
        request.forms.append('password_confirmation',
                request.forms.get('password'))

        # check for the consistency of all field
        # return only those field to be updated
        newuser = fieldparser.user_modify(user_info, request.forms)

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

        tplpage = template('admin/chuser', tpldata=user_info,
            user=cookie[0], flash=flash)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/rmuser', method='get')
def adm_chuser():
    cookie = _admin_auth()

    if cookie:
        uid = request.query.id
        tplpage = user.delete(cookie, uid)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/pricelists', method='get')
def adm_pricelists():
    cookie = _admin_auth()

    if cookie:
        tplpage = admin.pricelists(cookie)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/pricelists', method='post')
def adm_mail_pricelists():
    cookie = _admin_auth()

    if cookie:
        subject = request.forms.get('subject')
        msg = request.forms.get('message')
        user.mail_pricelists(cookie, subject, msg)
        flash = {'error':None, 'notice':'Spediti listini via email'}
        tplpage = admin.pricelists(cookie, flash)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/download_pricelist', method='get')
def adm_down_pl():
    cookie = _admin_auth()

    if cookie:
        pricelist = int(request.query.pl)
        filename = shop.download_pricelist(pricelist)

        if filename:
            return static_file(filename, root=config.path['private'], 
                    download=filename,
                    mimetype=config.pricelists['mimetype'])

@app.route('/admin/promo', method='get')
def adm_promo():
    cookie = _admin_auth()

    if cookie:
        tplpage = admin.promo(cookie)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/admin/promo', method='post')
def adm_mail_promo():
    cookie = _admin_auth()

    if cookie:
        subject = request.forms.get('subject')
        msg = request.forms.get('message')
        user.mail_promo(cookie, subject, msg)
        flash = {'error':None, 'notice':'Spedite promo via email'}
        tplpage = admin.promo(cookie, flash)
    else:
        tplpage = redirect('/')

    return (tplpage)

#
# User route
#

@app.route('/user/login', method='get')
def login_form():
    return template('user/login', error=None)

@app.route('/user/login', method='post')
def login_submit():
    email = request.forms.get('email')
    password = request.forms.get('password')
    # parse the input field
    email = fieldparser.email(email)
    password = fieldparser.password(password)

    if user.check_login(email, password):
        print "FIXME: login void the chart?"
        return redirect('/shop/index')
    else:
        return template('user/login', error="Login failed!")

@app.route('/user/add', method='get')
def user_add_get():
    tpldata = fieldparser.user_add(None)
    return template('user/add', tpldata=tpldata)

@app.route('/user/add', method='post')
def user_add_post():
    """ Add a new user """

    # check for the consistency of all field
    newuser = fieldparser.user_add(request.forms)

    if newuser['error'] is None:
        newuser = user.add(newuser)

        if newuser['error'] is None:
            newuser = fieldparser.user_add(None)
            newuser['notice'] = 'Registrazione inviata correttamente.'

    return template('user/add', tpldata=newuser)

@app.route('/user/modify', method='get')
def user_modify():
    cookie = _auth()

    if cookie:
        uid = user.uid(cookie)
        user_info = user.get_all_infos(uid)
        # add error and notice
        user_info['flash'] = None
        tplpage = template('user/modify', tpldata=user_info)
    else:
        tplpage = "Shit!"

    return (tplpage)

@app.route('/user/modify', method='post')
def user_modify():
    cookie = _auth()

    if cookie:
        flash = {'error':None, 'notice':None}
        uid = user.uid(cookie)
        user_info = user.get_all_infos(uid)
        # check for the consistency of all field
        # return only those field to be updated
        newuser = fieldparser.user_modify(user_info, request.forms)

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
        tplpage = template('user/modify', tpldata=user_info)
    else:
        tplpage = "Shit!"

    return (tplpage)

@app.route('/user/rmuser', method='get')
def user_del():
    cookie = _auth()

    if cookie:
        user.delete(cookie)

    # Remove the cookie
    user.logout()
    return redirect('/')

@app.route('/user/logout')
def logout():
    cookie = _auth()

    if cookie:
        shop.chart_del(user.uid(cookie))

    # Remove the cookie
    user.logout()
    return redirect('/')

#
# Shop route
#

@app.route('/shop/index', method='get')
def shop_index():
    cookie = _auth()

    if cookie:
        tplpage = shop.index(cookie)
    else:
        tplpage = "Shit!"

    return (tplpage)

@app.route('/shop/index', method='post')
def shop_index_submit():
    cookie = _auth()

    if cookie:
        cookie[1] = int(request.forms.get('codcat'))
        print "FIXME: default category not stored in the cookie"
        tplpage = shop.index(cookie)
    else:
        tplpage = "Shit!"

    return (tplpage)

@app.route('/shop/buy')
def shop_buy_article():
    # check if it is an ajax request
    if request.is_ajax:
        cookie = _auth()

        if cookie:
            # item id and quantity are a GET request.
            item_id = int(request.query.aid)
            item_qta = int(request.query.qta)
            uid = user.uid(cookie)
            shop.buy_item(uid, item_id, item_qta)
            return('OK')
        else:
            return('shit') # redirect to somewhere

@app.route('/shop/show')
def show_item():
    cookie = _auth()

    if cookie:
        # is a GET request
        item_id = int(request.query.aid)
        tplpage = shop.show_item(cookie, item_id)
    else:
        tplpage = redirect('/')

    return (tplpage)

@app.route('/shop/cart', method='get')
def shop_cart():
    cookie = _auth()

    if cookie:
        uid = user.uid(cookie)
        # get all infos about this uid from the dbase
        userinfo = user.get_all_infos(uid)
        tplpage = shop.shoppingcart(userinfo)
    else:
        tplpage = 'Shit'

    return (tplpage)

@app.route('/shop/cart', method='post')
def shop_cart():
    cookie = _auth()

    if cookie:
        item_id = int(request.forms.get('aid'))
        uid = user.uid(cookie)
        shop.buy_item(uid, item_id, 0)
        # get all infos about this uid from the dbase
        userinfo = user.get_all_infos(uid)
        tplpage = shop.shoppingcart(userinfo)
    else:
        tplpage = 'Shit'

    return (tplpage)

@app.route('/shop/checkout', method='post')
def shop_checkout():
    cookie = _auth()

    if cookie:
        uid = user.uid(cookie)
        user_info = user.get_all_infos(uid)
        # add the order information into the user dict.
        user_info['orderinfo'] = request.forms.get('info')
        tplpage = shop.checkout(user_info)
    else:
        tplpage = 'Shit'

    return (tplpage)

@app.route('/shop/download_pricelist')
def shop_download_pl():
    cookie = _auth()

    if cookie:
        filename = shop.download_pricelist(user.pricelist(cookie))

        if filename:
            return static_file(filename, root=config.path['private'], 
                    download=config.pricelists['filename'],
                    mimetype=config.pricelists['mimetype'])

@app.route('/shop/support')
def shop_support():
    cookie = _auth()

    if cookie:
        return template('store/support', tpldata=cookie[0])
    else:
        return ('Shit')

@app.route('/shop/info')
def shop_info():
    cookie = _auth()

    if cookie:
        return template('store/info', tpldata=cookie[0])
    else:
        return ('Shit')

@app.route('/shop/contacts')
def shop_contacts():
    cookie = _auth()

    if cookie:
        return template('store/contacts', tpldata=cookie[0])
    else:
        return ('Shit')

# Images route
@app.route('/images/<filename:re:.*\.png>')
def send_image(filename):
    basepath = os.path.join(config.path['base'], 'images')
    mypath = os.path.join(config.path['overlay'], 'images')

    if os.path.isfile(os.path.join(mypath, filename)):
        return static_file(filename, root=mypath, mimetype='image/png')
    else:
        return static_file(filename, root=basepath, mimetype='image/png')


# Static pages and files to be served.
@app.route('/static/<filename:path>')
def send_static(filename):
    basepath = os.path.join(config.path['base'], 'static')
    mypath = os.path.join(config.path['overlay'], 'static')

    if os.path.isfile(os.path.join(mypath, filename)):
        return static_file(filename, root=mypath)
    else:
        return static_file(filename, root=basepath)

if __name__ == "__main__":
    #run(host='localhost', port=8080, reloader=True)
    run(app, host='localhost', port=8080)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
