import json
import logging
import os
from ssm_parameter_store import SSMParameterStore
from smtp_email_sender import STMPEmail
from notification_config import NotificationConfig
from datetime import datetime
from locations import Location
from dateutil.parser import parse
from html_templater import Templater


def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def fetchData(event):
    
    data={}
    message=event['status']['messages']        

    location= Location(store)
    serialNo=message['alcolizer']['serialNo']
    results=location[int(serialNo)]
    data['location'],data['site']= location.parse(results)
    data['sets']=message['sets']
    data['serialNo']=serialNo

    dt=parse(message['date'])
    prettyDate=datetime.strftime(dt,'%d %B %Y : %H:%M:%S')
    data['datetime']=prettyDate

    return data

def createHtmlEmail(data):
    s3bucket = store['s3/bucket']
    htmltemplate=store['s3/email/status-html-template']

    sets=data['sets']
    
    message=''
    for row in sets:        
        message=message +'<tr><b>{}</b><br>{}<br>{} ({})</br>{}<br></td></tr>'.format(row['title'],row['group'],row['status'],row['id'],row['status decription']) 
    data['message'] = '<table>{}</table>'.format(message) 

    templater=Templater(Bucket=s3bucket,Template= htmltemplate )
    body=templater.combine(data)
    return body

def send(body,recipients):
    
    noReply = 'ibunney@fmgl.com.au'
    relay = store['email/smtp-server'] 

    smtpServer = STMPEmail( STMPServer= relay)
    smtpServer.set_subject('Alcolizer Rekognition Non-Negative Result!')
    smtpServer.set_sender(noReply)
    smtpServer.set_recipients(recipients)
    smtpServer.set_altTest('This is an email from the Alcolizer Rekognition!')
    
    try:
        smtpServer.send(body)  
    except Exception as e:               
        logger.exception("Could not send email.")
        logger.exception(e) 
        raise

def lambda_handler(event, context):
   
    global logger
    logger=establish_logger()
       
    hierarchy = 'dev' # os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )           
    
    data=fetchData(event)

    site=data['site']
    config=NotificationConfig(store,site)  
    mgr,emg,shut,second,contact=config.unpack()
    recipients=[emg]
    
    data['contact']=contact
        
    body=createHtmlEmail(data)    
    send(body,recipients)

    return {
        'Recipient': recipients
    }


