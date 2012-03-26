#!/usr/bin/env python

import re

class FieldParser:
    """
    Parser for input forms.
    """

    _re_email = None
    _re_pwd = None
    _re_text = None
    _re_piva = None

    def __init__(self):
        self._re_email = re.compile('^[A-Za-z0-9_.-]+@([A-Za-z0-9_]+\.)+[A-Za-z]{2,4}$')
        self._re_pwd = re.compile('^[a-zA-Z0-9]{6,10}$')
        self._re_text50 = re.compile('.{,50}')
        self._re_piva = re.compile('^[A-Za-z0-9]{1,20}$')

    def email(self, email):
        """ Check for a valid email string """

        if self._re_email.match(email):
            return (email)
        else:
            return (None)

    def varchar(self, string, maxlen):
        """ Check for a string from 1 char to maxlen. """
        pattern = '^[a-zA-Z0-9 _\.]{1,' + str(maxlen) + '}$'

        if re.match(pattern, string):
            return(string)
        else:
            return(None)

    def password(self, password):
        if self._re_pwd.match(password):
            return(password)
        else:
            return(None)

    def text(self, text):
        if self._re_text50.match(text):
            return(text)
        else:
            return(None)

    def piva(self, piva):
        if self._re_piva.match(piva):
            return(piva)
        else:
            return(None)

    def user_add(self, newuser):
        myuser = {'error': None,
                'notice': None,
                'email': '',
                'piva': '',
                'ragsoc': '',
                'respcom': '',
                'sede_via': '',
                'sede_civico': '',
                'sede_citta': '',
                'sede_prov': '',
                'sede_cap': '',
                'sede_stato': 'Italia',
                'sede_tel': '',
                'sede_fax': '',
                'sede_via_2': '',
                'sede_civico_2': '',
                'sede_citta_2': '',
                'sede_prov_2': '',
                'sede_cap_2': '',
                'sede_stato_2': 'Italia',
                'sede_tel_2': '',
                'sede_fax_2': '',
                'attivita': '',
                'email_listino': 't',
                'password': '',
                'password_confirmation': ''}

        if newuser:
            myuser['error'] = 'Error in:'

            for key in newuser:
                if key in myuser:
                    myuser[key] = newuser[key]

            # parse the email field
            if not self.email(myuser['email']):
                myuser['error'] += " email"
            
            # parse password field and check it with pass_confirm
            if self.password(myuser['password']) != myuser['password_confirmation']:
                myuser['error'] += ' password'

            # parse tax code field.
            if not self.piva(myuser['piva']):
                myuser['error'] += " piva"

            # parse Company name field.
            # convert to lowercase
            myuser['ragsoc'] = myuser['ragsoc'].lower()

            if not self.varchar(myuser['ragsoc'], 50):
                myuser['error'] += " Ragione Sociale"

            if len(myuser['error']) == 9:
                myuser['error'] = None
        else:
            myuser['error'] = None

        return (myuser)

    def user_modify(self, old, new):
        myuser = {'error':''}

        for key in new:
            if (key in old) and (old[key] != new[key]):
                myuser[key] = new[key]

        # parse the email field
        if ('email' in myuser) and (not self.email(myuser['email'])):
            myuser['error'] += " email"
        
        # parse password field and check it with pass_confirm
        if ('password' in myuser) and (self.password(myuser['password']) != new['password_confirmation']):
            myuser['error'] += ' password'

        if myuser['error']:
            myuser['error'] = "Errori in: " + myuser['error']
        else:
            myuser['error'] = None

        return (myuser)

if __name__ == "__main__":
    print "Cannot execute as program!"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
