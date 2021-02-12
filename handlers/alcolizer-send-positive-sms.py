import json
import logging
import os
import boto3 as bto
from ssm_parameter_store import SSMParameterStore
from datetime import datetime
from dateutil.parser import parse
from html_templater import Templater

SENDER_ID = 'Fortescue'
COUNTRY_PREFIX ='+61'

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def sendSMS( sns, mobile,body):
    response = sns.publish(
        PhoneNumber=mobile,
        Message=body,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {'DataType': 'String',
                                 'StringValue': SENDER_ID},
            'AWS.SNS.SMS.SMSType': {'DataType': 'String',
                                'StringValue': 'Transactional'}
        }
    )
    code = response['ResponseMetadata']['HTTPStatusCode']    
    logger.info('Response [%s] for SMS Message [%s] was sent to mobile [%s].',code, body, mobile)

    return code

def createtextMsg(data):
    s3bucket = store['s3/bucket']
    txtTemplate=store['s3/sms/text-msg-template']

    templater=Templater(Bucket=s3bucket,Template= txtTemplate )
    body=templater.combine(data)
    return body


def lambda_handler(event, context):

    code='500'

    global logger
    logger=establish_logger()
       
    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )        

    # should only be 1 record
    for rec in event['Records']:
        
        content= rec['Sns']['Message']           
        data= json.loads(content)      

        region = store['dynamoDB/region'] # all artifacts in same region  
        msg = createtextMsg(data)
        targets = data['recipients']

        sns = bto.client('sns',region_name=region)     
        mobile ='{}{}'.format(COUNTRY_PREFIX,targets['mobile'])
       
             
        blocked = store['notification/blocked']        
        if blocked != 'TRUE' :
            code=sendSMS(sns,mobile,msg)    
    
    result = {
        'statusCode': code,
        'blocked' : blocked,
        'Recipient': targets
    }
        
    logger.info('SMS SNS Complete [%s].', result)

    return result

