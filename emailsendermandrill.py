import requests
from confutil import ConfUtil 
import json

class EmailSenderMandrill:
    """
    This is the email sender class using the MANDRILL implementation
    It gets the configuration from file mandrill.conf 
    """
    def __init__(self):
        self._conf = ConfUtil('emailsender.conf')
        
        
    def send(self, from_email, to_list, subject, text):
        """
        this is to acutally send the email
        
        Here the input parameter are all validated.
        We can assume they are all good.
        
        from_email is one single email address
        to_list is a list of email address
        
        return 0 if the sending sucess
        return 1 if the sending failed
        return 5 if the configuration is not complete
        """
        api_url = self._conf.get('mandrill_api_url');
        key = self._conf.get('mandrill_key');
        
        to = ','.join(to_list)
        
        if not api_url or not key:
            return 5, 'configuration not complete'
        else:
            
            
            
            to_address_list = []
            
            for to_address in to_list:
                to_address_list.append(
                    {
                        "email":to_address,
                        "type":"to"
                    }
                )

            
            mandrill_data = {
                "key":key,
                "message":{
                    "text":text,
                    "subject":subject,
                    "from_email":from_email,
                    "to":to_address_list
                },
                "async":False,
                "send_at":"2014-07-01 00:00:00"
            }
            
            
            
            
            response = requests.post(
                api_url,
                data=json.dumps(mandrill_data)
            )
            
            #print response.content    
               
            if response.ok:
                status = 0
            else:
                status = 1
                
            message = str(response.content)
          
                            
                            
            return status, message
                
        
    
    
    
    
    