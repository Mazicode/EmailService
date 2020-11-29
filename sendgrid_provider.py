import requests
from sendgrid import SendGridAPIClient

from emailservice.config import sendgrid_key, sendgrid_url
import json


class SendgridProvider:
    """
    This is the email sender class using the MANDRILL implementation
    It gets the configuration from file mandrill.conf
    """

    def __init__(self):
        self.client = SendGridAPIClient('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').client
        # self._conf = ConfUtil('emailsender.conf')

    def send(self, from_email, to_list, cc_list, bcc_list, subject, text):
        """
        this is to actually send the email

        """

        to_address_list = []

        if len(to_list) > 0:
            for to_address in to_list:
                to_address_list.append(
                    {
                        "email": to_address,
                        "type": "to"
                    }
                )

        if len(cc_list) > 0:
            for cc_address in cc_list:
                to_address_list.append(
                    {
                        "email": cc_address,
                        "type": "cc"
                    }
                )

        if len(bcc_list) > 0:
            for bcc_address in bcc_list:
                to_address_list.append(
                    {
                        "email": bcc_address,
                        "type": "bcc"
                    }
                )

        sendgrid_data = {
            "key": sendgrid_key,
            "message": {
                "text": text,
                "subject": subject,
                "from_email": from_email,
                "to": to_address_list
            },
            "async": False,
        }

        response = requests.post(
            sendgrid_url,
            data=json.dumps(sendgrid_data)
        )

        if response.ok:
            status = 0
        else:
            status = 1

        message = str(response.content)

        return status, message
