import json
import logging
import os
from ssm_parameter_store import SSMParameterStore
from smtp_email_sender import STMPEmail
from html_templater import Templater
from datetime import datetime
from dateutil.parser import parse

EVENT='event'
ALCOLIZER_RESULT='alcolizerResult'
ALCOHOL='internalValue'

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def createHtmlEmail(data):
    s3bucket = store['s3/bucket']
    htmltemplate=store['s3/email/breathresult-html-template']

    templater=Templater(Bucket=s3bucket,Template= htmltemplate )
    body=templater.combine(data)
    return body

def send(body,recipients):
    
    noReply = store['ses/noreply']
    region  = store['dynamoDB/region'] 

    smtpServer = STMPEmail( Region =region)
    smtpServer.set_subject('Alcolizer Rekognition Non-Negative Result!')
    smtpServer.set_sender(noReply)
    smtpServer.set_recipients(recipients)
    smtpServer.set_altTest('This is an email from the Alcolizer Rekognition!')
    
    return smtpServer.send(body)  
    
def lambda_handler(event, context):

    code=200
    message='Email was withheld'

    global logger
    logger=establish_logger()
       
    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    # add 'SecondaryBreathTestLocation, 'ContactPhone' from connfig to email data
  
    for rec in event['Records']:
        content= rec['Sns']['Message']   
        data= json.loads(content)      
    
        recipients= data['recipients']['email']
        logger.info('Supplied message data [%s]',data)
    
        body=createHtmlEmail(data)     

        blocked = store['notification/blocked']
        if blocked != 'TRUE' :
            message= send(body,recipients)  
        
        result= {
                'blocked' : blocked,
                'response' : message
        }

        logger.info('Email Notification Response [%s].', result)
        return result