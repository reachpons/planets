import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEPARATOR = ', '

class STMPEmail(object):

    def __init__(self, STMPServer):
        self._server=STMPServer
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
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self._subject
        msg['From'] = self._sender

        to= SEPARATOR.join(self._recipients)
        msg['To'] = to

        text = self._altText
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(body, 'html')

        msg.attach(part1)
        msg.attach(part2)

        s = smtplib.SMTP(self._server)
        s.sendmail(self._sender, self._recipients, msg.as_string())       
        s.quit()

