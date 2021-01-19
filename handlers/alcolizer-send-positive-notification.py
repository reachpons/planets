import json
import logging
import os
from ssm_parameter_store import SSMParameterStore
from smtp_email_sender import STMPEmail
from html_templater import Templater
from employee_detail import EmployeeDetail
from datetime import datetime
from dateutil.parser import parse
from notification_rule import NotificationRule

EVENT='event'
ALCOLIZER_RESULT='alcolizerResult'
ALCOHOL='internalValue'

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def fetchData(event): 

    # extract Weighted SAPID
    sapid=event['event']['weighted']['sapid']
    
    # fetch data from SucessFactors
    employees=EmployeeDetail(APIEndpoint='Sucessfactors.fmgl.com.au')    
    detail = employees.fetch(sapid)

    # Create a Single data blob for HTML Combine

    employee=detail['employee']
    supervisor=detail['supervisor']
    result=event['event']['alcolizerResult']
    
    dt=parse(result['alcolizerDateTime'])
    prettyDate=datetime.strftime(dt,'%d %B %Y : %H:%M:%S')

    data= {
            'surname' : employee['surname'],
            'givenNames' : employee['firstName'],
            'shift' :'Day',
            'department' : employee['department'],
            'supervisorSurname' : supervisor['surname'],
            'supervisorGivenNames' : supervisor['firstName'],
            'datetime' : prettyDate,
            'alcolizer' :result['serialNo'],
            'displayedResult' : result['resultDisplayedText'],
            'company' :' Fortescue Metals Group',
            'site' : result['site'],
            'location' : result['location']            
        }

    return data,detail,result['site']

def createHtmlEmail(data):
    s3bucket = store['s3/bucket']
    htmltemplate=store['s3/email/html-template']

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


def lambda_handler(event, context):

    global logger
    logger=establish_logger()
       
    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )
           
    emailData,employeeData,site=fetchData(event)
   

    # rule rules set of employeeData tyo determine recipient
    rule = NotificationRule(store,site)
    recipients=rule.evaluate(employeeData)

    # add 'SecondaryBreathTestLocation, 'ContactPhone' from connfig to email data
    emailData['secondaryLocation']=rule.secondaryLocation()
    emailData['contact']=rule.contact()
        

    body=createHtmlEmail(emailData)
    send(body,recipients)

    return {
        'Recipient': recipients
    }

