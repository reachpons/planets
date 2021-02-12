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
    #logger.info('Response [%s] for SMS Message [%s] was sent to mobile [%s].',code, body, mobile)
    print(response)    
    return code

def createtextMsg(data):
    s3bucket = store['s3/bucket']
    txtTemplate=store['s3/sms/text-msg-template']

    templater=Templater(Bucket=s3bucket,Template= txtTemplate )
    body=templater.combine(data)
    return body


def main4():
    msg="""Please be advised that Bunney, Ian Bruce has had a non-negative breath alcohol concentration result and requires a confirmatory test to be completed within 20 minutes.
Date & Time : 14 September 2020 : 09:12:42
Alcolier location: Level 3 - Security Build Desk 
Alcolier Serial #:  33000695
Result : 0.049 g/100mL BAC"""
    sns = bto.client('sns',region_name='ap-southeast-2')     
    mobile = '{} {}'.format(COUNTRY_PREFIX,'0439983596' )

    code=sendSMS(sns,mobile,msg)  
    print(code)


def main():
    
    global logger
    logger=establish_logger()
       
    hierarchy = 'dev' #os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )
    
    blocked = store['notification/blocked']

    print( blocked)
    print(blocked != 'TRUE')
    

    return 

    data= {
            "default": "Alcolizer Rekognition - this message can be ignored.",
            "surname" : "Bunney",
            "givenNames" : "Ian",
            "shift" :"Day",
            "department" :  "Technology & Automation",
            "supervisorSurname" : "Lewis",
            "supervisorGivenNames" : "Shelley",
            "datetime" : "3 Feburary 2021: 11:30AM",
            "alcolizer" :"310210335",
            "displayedResult" : "0.003 g/100Ml BAC",
            "company" :" Fortescue Metals Group",
            "site" : "Fortescue Centre",
            "location" : "Level 3 - Security Build desk",
            "secondaryLocation" : " Level Kitchen",
            "recipients" : {
                "email" : ["ibunney@fmgl.com.au"],
                "mobile" : "0439983596"       
            }            
    }

    region = store['dynamoDB/region']
    msg = createtextMsg(data)
    targets = data['recipients']

    sns = bto.client('sns',region_name=region)     
    mobile ='{}{}'.format(COUNTRY_PREFIX,targets['mobile'])
    sendSMS(sns,mobile,msg)    


def main2():
    
    data= {
            "default": "Alcolizer Rekognition - this message can be ignored.",
            "surname" : "Bunney",
            "givenNames" : "Ian",
            "shift" :"Day",
            "department" :  "Technology & Automation",
            "supervisorSurname" : "Lewis",
            "supervisorGivenNames" : "Shelley",
            "datetime" : "3 Feburary 2021: 11:30AM",
            "alcolizer" :"310210335",
            "displayedResult" : ".0003 g/100Ml BAC",
            "company" :" Fortescue Metals Group",
            "site" : "Fortescue Centre",
            "location" : "Level 3 - Security Build desk",
            "secondaryLocation" : " Level Kitchen",
            "recipients" : {
                "email" : ["ibunney@fmgl.com.au"],
                "mobile" : "0439983596"       
            }            
    }
    message = json.dumps({
            'default': json.dumps(data)
            })
    sns = bto.client('sns',region_name='ap-southeast-2')

    response = sns.publish(
                    TopicArn = 'arn:aws:sns:ap-southeast-2:317510107845:Alcolizer-Rekognition-Notification',
                    Message = message,
                    MessageStructure='json' )
          
    print (response)

    

if __name__ == "__main__":
    main()
