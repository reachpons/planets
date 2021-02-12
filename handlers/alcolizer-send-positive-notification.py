import json
import logging
import os
import boto3 as bto
from ssm_parameter_store import SSMParameterStore
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

def fetchEmployeeData(sapid):
    
    # fetch data from SucessFactors
    employees=EmployeeDetail(sapid)    
    return employees.fetch()

def buildData(event): 

    # extract Weighted SAPID
    sapid=event['event']['weighted']['sapid']
    # TODO Check for confidence 
    
    if len(sapid) == 0 :
        return None,None,None

    detail=fetchEmployeeData(sapid)
        
    # Create a Single data blob for HTML Combine
    employee=detail['employee']
    supervisor=detail['supervisor']
    result=event['event']['alcolizerResult']
    
    dt=parse(result['alcolizerDateTime'])
    prettyDate=datetime.strftime(dt,'%d %B %Y : %H:%M:%S')
                
    data= {
            'surname' : employee['surname'],
            'givenNames' : employee['firstName'],            
            'department' : employee['department'],
            'supervisorSurname' : supervisor['surname'],
            'supervisorGivenNames' : supervisor['firstName'],
            'datetime' : prettyDate,
            'alcolizer' :result['serialNo'],
            'displayedResult' : result['resultDisplayedText'],
            'company' :' Fortescue Metals Group',
            'site' : result['site'],
            'location' : result['location'],
            'similarity' : event['event']['weighted']['similarity'],
            'confidence' : event['event']['weighted']['confidence']
        }

    return data,detail,result['site']


def sendSNS(msg):  
    topic = store['sns/topic/notification']
    region = store['dynamoDB/region'] # all artifacts in same region  
    
    message = json.dumps({'default': json.dumps(msg)})
    sns = bto.client('sns',region_name=region)

    response = sns.publish(
                    TopicArn = topic,
                    Message = message,
                    MessageStructure='json' )
    code = response['ResponseMetadata']['HTTPStatusCode']    
    return code

def lambda_handler(event, context):

    global logger
    logger=establish_logger()
       
    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )
           
    msgData,employeeData,site=buildData(event)

    if employeeData is None:
        return {
            'statusCode' : 200,
            'Recipient': 'No Identity'
        }
   
    # rule rules set of employeeData tyo determine recipient
    rule = NotificationRule(store,site)
    emails,mobileNo=rule.evaluate(employeeData)

    # add 'SecondaryBreathTestLocation, 'ContactPhone' from connfig to email data
    msgData['secondaryLocation']=rule.SecondaryLocation()       
    
    recipients = {
        'email' : emails ,
        'mobile' : mobileNo       
    }
    
    msgData['recipients']=recipients
    
    pout=json.dumps(msgData,indent=4 )
    logger.info('SNS Message => Event[{}]'.format( pout  ))

    code=sendSNS(msgData)

    return {
        'statusCode' : code,
        'Recipient': recipients
    }


