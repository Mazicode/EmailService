from flask import Flask
# from flask.ext.mandrill import Mandrill
# from flask_mailgun import MailGun


class ReverseProxied(object):
    """Middleware for handling reverse proxied setups."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        forwarded_proto = environ.get("HTTP_X_FORWARDED_PROTO", "")
        forwarded_for = environ.get("HTTP_X_FORWARDED_FOR", "").split(",")[0]
        forwarded_host = environ.get("HTTP_X_FORWARDED_HOST", "")

        if script_name:
            environ["SCRIPT_NAME"] = script_name
        if forwarded_for is not None:
            environ["REMOTE_ADDR"] = forwarded_for
        if forwarded_host:
            environ["HTTP_HOST"] = forwarded_host
        if forwarded_proto:
            environ["wsgi.url_scheme"] = forwarded_proto
        return self.app(environ, start_response)


def create_app(test_config=None):
    app = Flask(__name__)
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.config.from_object('emailsender.config')

    # # app.config['MANDRILL_API_KEY'] = 'your api key'
    # mandrill = Mandrill(app)
    # mandrill.send_email(
    #     from_email='someone@yourdomain.com',
    #     to=[{'email': 'someoneelse@someotherdomain.com'}],
    #     text='Hello World'
    # )

