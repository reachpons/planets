import boto

SEPARATOR = ', '
CHARSET = "UTF-8"

# this class now uses the AWS SES API rather than an SMTP Server
class STMPEmail(object):

    def __init__(self, Region):
        self._region=Region
        self._recipients=[]
        self._sender=None
        self._subject=None  
        self._altText='FMG Email'      
    
    def set_subject(self,val):
        self._subject = val

    def set_sender(self,val):
        self._sender = val

    def set_recipients(self,val):
        self._recipients=val
    
    def set_altTest(self,val):
        self._altText=val

    def send(self,body):        

        if self._sender is None or  self._subject is None or self._recipients.count == 0 :
            return 
        
        to= SEPARATOR.join(self._recipients)       
        client = boto3.client('ses',region_name=self._region)

        try:   
            response = client.send_email(
                Destination={
                    'ToAddresses': to
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': body,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': self._altText,
                        }
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': self._subject,
                    },
                },
                Source=self._sender
            )

        except ClientError as e:
            return {
                'statusCode' : 500 ,
                'message' : e.response['Error']['Message'])
            }

        return {
            'statusCode' : 200,
            'Recipient': { to }
        }         
