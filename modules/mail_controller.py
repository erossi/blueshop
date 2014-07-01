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

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# for templating the mail messages
from bottle import template

class MailUtils:
    """A simple example class"""

    # configuration parameters
    _config = None

    def __init__(self, config):
        self._config = config

    def _send(self, myfrom, bcc, composed):
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP(self._config.mail['smtp'])
        ok = True

        try:
            s.sendmail(myfrom, bcc, composed)
        except Exception, e:
            errorMsg = "Unable to send email. Error: %s" % str(e)
            print errorMsg
            ok = False

        s.quit()
        return(ok)

    def recover_password(self, myuser):
        """
        Send an email with the password to a registered user.
        """

        # Create a text/plain message
        msg = template('mail/recover_password', tpldata=myuser)
        msg = MIMEText(msg)
        msg['From'] = self._config.mail['recover_pwd_from']
        msg['To'] = myuser[0]
        msg['Subject'] = self._config.mail['recover_pwd_subject']
        composed = msg.as_string()
        ok = self._send(msg['from'], msg['To'], composed)
        return(ok)

    def add_user(self, myuser):
        """
        Send an email to the operator to signal the new
        user registation's request.
        """

        # Create a text/plain message
        msg = template('mail/new_user_request', tpldata=myuser)
        msg = MIMEText(msg)
        msg['From'] = self._config.mail['newuser_from']
        msg['To'] = self._config.mail['newuser_to']
        msg['Subject'] = self._config.mail['newuser_subject']
        composed = msg.as_string()
        ok = self._send(msg['from'], msg['To'], composed)
        return(ok)

    def shop_checkout(self, tpldata):
        """ Send the order to the customer and the company.
        """
        # Create a text/plain message
        msg = template('mail/shop_send_order', tpldata=tpldata)
        msg = MIMEText(msg)
        msg['From'] = self._config.mail['neworder_from']
        msg['To'] = tpldata['user']['email']
        msg['Subject'] = self._config.mail['neworder_subject']
        bcc = (self._config.mail['neworder_bcc'], msg['To'])
        composed = msg.as_string()
        return(self._send(msg['from'], bcc, composed))

    def pricelists(self, filetosend, emails, subject, msg):
        outer = MIMEMultipart()
        outer['From'] = self._config.mail['pricelist_from']
        outer['To'] = self._config.mail['pricelist_to']
        outer['Subject'] = subject
        outer.preamble = 'This is a multi-part message in MIME format.\n'
        # Attach text message
        msg = MIMEText(msg)
        outer.attach(msg)
        # Attach xls file
        fp = open(filetosend, 'rb')
        maintype, subtype = self._config.pricelists['mimetype'].split('/', 1)
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(fp.read())
        fp.close()
        # Encode the payload using Base64
        encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment',
                filename=self._config.pricelists['filename'])
        outer.attach(msg)
        composed = outer.as_string()

        # send the email
        bcc = []
        s = smtplib.SMTP(self._config.mail['smtp'])

        for i in emails:
            bcc.append(i[0])

            if not (len(bcc) % self._config.mail['bcc_limit']):
                try:
                    s.sendmail(self._config.mail['from'], bcc, composed)
                except Exception, e:
                    errorMsg = "Unable to send email. Error: %s" % str(e)
                    print errorMsg

                bcc = []

        if len(bcc):
            try:
                s.sendmail(self._config.mail['from'], bcc, composed)
            except Exception, e:
                errorMsg = "Unable to send email. Error: %s" % str(e)
                print errorMsg

        s.quit()

    def promo(self, emails, subject, msg):
        """
        """
        # Create a text/plain message
        msg = MIMEText(msg)
        msg['From'] = self._config.mail['promo_from']
        msg['To'] = self._config.mail['promo_to']
        msg['Subject'] = subject

        composed = msg.as_string()

        # send the email
        bcc = []
        s = smtplib.SMTP(self._config.mail['smtp'])

        for i in emails:
            bcc.append(i[0])

            if not (len(bcc) % self._config.mail['bcc_limit']):
                try:
                    s.sendmail(self._config.mail['from'], bcc, composed)
                except Exception, e:
                    errorMsg = "Unable to send email. Error: %s" % str(e)
                    print errorMsg

                bcc = []

        if len(bcc):
            try:
                s.sendmail(self._config.mail['from'], bcc, composed)
            except Exception, e:
                errorMsg = "Unable to send email. Error: %s" % str(e)
                print errorMsg

        s.quit()

if __name__ == "__main__":
    print "Cannot execute as program!"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
