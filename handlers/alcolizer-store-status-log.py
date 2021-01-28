import boto3 as bto
import json
import logging
import os
from ssm_parameter_store import SSMParameterStore
from datetime import datetime
import uuid
from urllib.parse import unquote
from locations import Location


EVENT='event'
ID='id'

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def parseIdentification(dict):
    data={}
    if dict is None: return None

    serialNo=dict.get('serial')['value']
    data['serialNo']=serialNo
    data['software']=dict.get('software')['value']
    data['assembly']=dict.get('assembly')['value']

    location= Location(store)
    results=location[int(serialNo)]
    data['location'],data['site']= location.parse(results)
    return data

def loadAttachment(s3bucket,s3key):
    s3 = bto.resource('s3')
    
    unkey = unquote(s3key)
    obj = s3.Object(s3bucket, unkey)
    
    body = obj.get()['Body'].read()
    return json.loads(body)

def buildStatusReport(raw,machine):
    if raw is None: return None

    dateStr= datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]    
    
    groups=raw.get('groups')
    sets=raw.get('set')
    rslts=[]
    for st in sets:        
        grp=st['group']        
        group=groups[grp]
        rs={
            'title' : group['ui_title'],
            'group' : group['ui_description'],            
            'status' : st['ui_title'],
            'id'  : st['id'],
            'status decription' : st['ui_description']
        }
        rslts.append(rs)
 
    return {
        'date' : dateStr,
        'alcolizer' : machine,
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
    return ix
    

def lambda_handler(event, context):

    hierarchy = os.environ['hierarchy']

    global logger
    logger=establish_logger()
    
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    bucket = event['email']['bucket']
    key = event['email']['key']

    raw =loadAttachment(bucket,key)
    machine=parseIdentification(raw.get('identification'))

    content= buildStatusReport(raw,machine) 
  
    output= json.dumps(content,indent=4) 
    ixKey=storeStatusLogToS3(output)

    return {
        'sucesss': 200,
        'key' : ixKey,
        'messages' : content
    }
