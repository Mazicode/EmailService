"""
This is the test cases of the email service

"""
from emailservice.mailgun_provider import MailGunProvider
from emailservice.sendgrid_provider import SendgridProvider
from emailservice.emailservice import EmailService
from emailservice.app import app

client = app.test_client()
mailgun = MailGunProvider()
sendgrid = SendgridProvider()


def test_endpoint():
    success_request = client.post('/', data={'subject': "something", "from": "marco.zingales88@gmail.com",
                                             "to_list": ["marzi@dtu.dk"], "CC": [], "BCC": [], "text": "something"},
                                  content_type='multipart/form-data'
                                  )
    assert success_request.status_code == 400, success_request


def _test(text, passed):
    output = ''
    if passed:
        output += 'Pass  : '
    else:
        output += 'Fail! : '
    output += text


def test_mailgun():
    """
    This is to test the MailGun implementation EmailSenderMailGun
    """

    status, message = mailgun.send('marco.zingales@gmail.com', ['marzi@dtu.dk'], ['hello there'], [], 'test1',
                                   'testcontent1')
    _test("mailgun works", status == 0)


def test_mailgun_only_cc():
    """
    This is to test the MailGun implementation EmailSenderMailGun
    """
    status, message = mailgun.send('marco.zingales@gmail.com', [], ['marzi@dtu.dk'], [], 'test1', 'testcontent1')
    _test("mailgun cannot send email without to", status == 1)


def test_mailgun_only_bcc():
    """
    This is to test the MailGun implementation EmailSenderMailGun
    """
    status, message = mailgun.send('marco.zingales@gmail.com', [], [], ['marzi@dtu.dk'], 'test1', 'testcontent1')
    _test("mailgun cannot send email without to", status == 1)


def test_mandrill():
    """
    This is to test the Mandrill implementation EmailSenderMandrill
    """
    status, message = sendgrid.send('marco.zingales@gmail.com', ['marzi@dtu.dk'], [], [], 'test', 'testcontent')
    _test("mandrill works", status == 0)


def test_mandrill_only_cc():
    """
    This is to test the Mandrill implementation EmailSenderMandrill
    """
    status, message = sendgrid.send('marco.zingales@gmail.com', [], ['marzi@dtu.dk'], [], 'test mandrill only cc',
                                    'testcontent')
    _test("mandrill works without to", status == 0)


def test_mandrill_only_bcc():
    """
    This is to test the Mandrill implementation EmailSenderMandrill
    """
    status, message = sendgrid.send('marco.zingales@gmail.com', [], [], ['marzi@dtu.dk'], 'test mandril only bcc',
                                    'testcontent')
    _test("mandrill works without to", status == 0)


def test_emailservice_validation():
    """
    This is to test the email address validation function in EmailService
    """

    emailService = EmailService()
    _test("emailService.validate_email_address('marzi@dtu.dk')",
          (bool(emailService.validate_email_address('marzi@dtu.dk'))))
    _test("emailService.validate_email_address('marzi@dtu.dk')",
          (bool(emailService.validate_email_address('marzi@dtu.dk'))))
    _test("not emailService.validate_email_address('@gmail.com')",
          (bool(not emailService.validate_email_address('@gmail.com'))))
    _test("not emailService.validate_email_address('test@gmail')",
          (bool(not emailService.validate_email_address('test@gmail'))))


def test_emailservice_send():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email("marco.zingales@gmail.com", ["marco.zingales@gmail.com"],
                                              ["marco.zingales@gmail.com"],
                                              "marzi@dtu.dk", "test subject 101", "test content 102")
    _test('send email', status == 0)


def test_emailservice_send_invalid_from():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email(None, ["xxx"], "yyyy", "marco.zingales@gmail.com",
                                              "test subject only bcc",
                                              "test content 102")
    _test("validate from", status == 1)


def test_emailservice_send_invalid_from1():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email('xxxxx', ["xxx"], "yyyy", "marco.zingales@gmail.com", "test subject",
                                              "test content 102")
    _test("validate from", status == 1)


def test_emailservice_send_invalid_subject_text_empty():
    """
    This is to test sending emails in EmailService
    """
    emailservice = EmailService()
    status, message = emailservice.send_email('marco.zingales@gmail.com', ["xxx"], "yyyy", 'marzi@dtu.dk', None, "")
    _test("validate subject/text", status == 3)
