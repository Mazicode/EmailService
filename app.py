#!../bin/python
import os

import requests
from flask import Flask, jsonify, request
from emailservice.emailservice import EmailService
from emailservice.config import mailgun_api_url, mailgun_key

# from flask.ext.mandrill import Mandrill

"""
This is the web interface of the email service API. It serves the REST API requests. 

The url is like
/emailservice/api/v1.0/sendemail, the main API
/emailservice/api/v1.0/sendemail/help, for help

"""

app = Flask(__name__)
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# app.config.from_object('emailsender.config')


@app.route('/', methods=['POST'])
def send_email():
    """
    This is to serve the main API of the email service.
    It take a JSON input and uses it as arg for the email to send.
    """

    form_fields = request.form
    status, message = EmailService().send_email(form_fields['from'], form_fields['to_list'], form_fields['CC'],
                                                form_fields['BCC'], form_fields['subject'], form_fields['text'])

    return jsonify({'status': status, 'message': message})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
