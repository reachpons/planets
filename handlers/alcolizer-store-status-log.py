import boto3 as bto
import json
import logging
import os
from ssm_parameter_store import SSMParameterStore
from datetime import datetime
import uuid
from urllib.parse import unquote

EVENT='event'
ID='id'

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr


def loadAttachment(s3bucket,s3key):
    s3 = bto.resource('s3')
    
    unkey = unquote(s3key)
    obj = s3.Object(s3bucket, unkey)
    
    body = obj.get()['Body'].read()
    return json.loads(body)

def buildStatusReport(raw):
    if raw is None: return None

    groups=raw.get('groups')
    sets=raw.get('set')
    rslts=[]
    for st in sets:        
        grp=st['group']
        group=groups[grp]
        rs={
            'title' : group['ui_title'],
            'group' : group['ui_description'],            
            'status' : st['ui_description'],
            'status decription' : st['ui_description']
        }
        rslts.append(rs)
 
    return {
        'sets' : rslts 
    }



def storeStatusLogToS3(output):

    eventid=str(uuid.uuid1())

    s3bucket = store['s3/bucket']
    s3Key = store['s3/statusLogKey']
    
    utcDateIssued=datetime.utcnow()
    ix='{}year={}/month={}/day={}/{}.json'.format(s3Key,utcDateIssued.year,utcDateIssued.month,utcDateIssued.day,eventid)

    s3Client = bto.client('s3')
    response = s3Client.put_object( Bucket=s3bucket,
                                    Body=output,
                                    Key=ix,
                                    Metadata = {'eventId': eventid },
                                    ContentType= 'application/json' )
    

def lambda_handler(event, context):

    hierarchy = os.environ['hierarchy']

    global logger
    logger=establish_logger()
    
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    bucket = event['email']['bucket']
    key = event['email']['key']

    raw =loadAttachment(bucket,key)
    content= buildStatusReport(raw) 

    output= json.dumps(content,indent=4) 
    storeStatusLogToS3(output)

    return {
        'sucesss': 200,
        'messages' : content
    }
