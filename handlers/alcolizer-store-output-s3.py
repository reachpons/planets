import boto3 as bto
import json
import logging
import os
from ssm_parameter_store import SSMParameterStore
from datetime import datetime

EVENT='event'
ID='id'

def storeToS3(id,output):
    s3bucket = store['s3/bucket']
    s3outputKey = store['s3/outputKey']
    
    utcDateIssued=datetime.utcnow()
    #'{}{}.json'.format(s3outputKey,id)
    ix='{}year={}/month={}/day={}/{}.json'.format(s3outputKey,utcDateIssued.year,utcDateIssued.month,utcDateIssued.day,id)

    s3Client = bto.client('s3')
    response = s3Client.put_object( Bucket=s3bucket,
                                    Body=output,
                                    Key=ix,
                                    Metadata = {'eventId': id },
                                    ContentType= 'application/json' )
        

def lambda_handler(event, context):

    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    eventid= event[EVENT][ID]    
    output= json.dumps(event,indent=4) 

    storeToS3(eventid,output)

    return {
        'statusCode': 200,
        'response': "End"
    }
