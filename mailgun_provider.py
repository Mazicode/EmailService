import requests
from emailservice.config import mailgun_key, mailgun_api_url


class MailGunProvider:
    """
    This is the email sender class using the MailGun implementation.
    The interface is send(self, from_email, to_list, cc_list, bcc_list, subject, text)
    """

    def send(self, from_email, to_list, cc_list, bcc_list, subject, text):
        """
        this is to actually send the email
        
        from_email is one single email address
        to_list is a list of email address. It could be an empty list.
        cc_list is a list. It could be an empty list.
        bcc_list is a list. It could be an empty list.
        
        here, we can assume the input parameters are all valid
        
        return 0 if the sending success
        return 1 if the sending failed
        return 5 if the configuration is not complete
        """

        data_dict = {'from': from_email,
                     'subject': subject,
                     'text': text
                     }

        if len(to_list) > 0:
            data_dict['to'] = ','.join(to_list)

        if len(cc_list) > 0:
            data_dict['cc'] = ','.join(cc_list)

        if len(bcc_list) > 0:
            data_dict['bcc'] = ','.join(bcc_list)

        response = requests.post(
            mailgun_api_url,
            auth=('api', mailgun_key),
            data=data_dict)

        if response.ok:
            status = 0
        else:
            status = 1
        message = str(response.content)

        return status, message
