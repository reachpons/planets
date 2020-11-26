import boto3 as bto
import json
import logging
import email
import uuid
import logging
from urllib.parse import unquote
from ssm_parameter_store import SSMParameterStore
from datetime import datetime


def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def loadfile(s3bucket,s3key):
    s3 = bto.resource('s3')
    
    unkey = unquote(s3key)
    obj = s3.Object(s3bucket, unkey)
    
    body = obj.get()['Body'].read()
    return body

def isJSON(content):
  try:
    json_object = json.loads(content)
  except ValueError as e:
    return False
  return True

def chevronLess(whole):
    rslt=whole[whole.find('<')+1 : whole.rfind('>')]
    return rslt

def storeToS3(output,partName):
    
    attachmentId=str(uuid.uuid1())

    suffix=partName.split('.')[0]
    s3bucket = store['s3/bucket']
    s3outputKey = store['s3/attachmentKey']
    
    utcDateIssued=datetime.utcnow()   
    ix='{}year={}/month={}/day={}/{}-{}.json'.format(s3outputKey,utcDateIssued.year,utcDateIssued.month,utcDateIssued.day,suffix,attachmentId)
    
    s3Client = bto.client('s3')
    response = s3Client.put_object( Bucket=s3bucket,
                                    Body=output,
                                    Key=ix,
                                    ContentType= 'application/json',
                                    ACL='bucket-owner-full-control' )
    return ix

def getAttachment(content):
   
    decoded = content.decode('utf-8') 
    msg = email.message_from_string(decoded)  # ? encoding = 'ISO-8859-1'
    msg_content_type = msg.get_content_type()
    
    attachmentName=None
    for part in msg.walk():

        if part.get_content_maintype() == 'multipart':            
            continue

        disposition=part.get('Content-Disposition')
        if disposition is None:
            continue

        partName=part.get_filename()
        partPay=part.get_payload(decode=True)
        if isJSON(partPay)  and '.json' in partName :            
            attachmentName = storeToS3(partPay,partName)

    return attachmentName

def lambda_handler(event, context):

    global logger
    logger=establish_logger()

    #hierarchy = os.environ['hierarchy']
    hierarchy='dev'
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )


    emailBucket = event['Records'][0]['s3']['bucket']['name']
    emailKey = event['Records'][0]['s3']['object']['key']
        
    email=loadfile(emailBucket,emailKey)

    attachmentKey=getAttachment(email)
    attachmentBucket=store['s3/bucket']
       
    return {
            'statusCode': 200,     
            'email' : {
                    'bucket' : attachmentBucket,
                    'key' : attachmentKey
                }
        }   
