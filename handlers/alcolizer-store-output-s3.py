import boto3 as bto
import json
import logging

logger=None
EVENT='event'
ID='id'


def getParameter(name):
    ssm = bto.client('ssm')
    parameter = ssm.get_parameter(Name=name, WithDecryption=False)['Parameter']
    return parameter['Value']

def storeToS3(id,output):
    s3bucket = getParameter('/alcolizer-rekognition/s3/bucket')
    s3outputKey = getParameter('/alcolizer-rekognition/s3/outputKey')
      
    s3Client = bto.client('s3')
    response = s3Client.put_object( Bucket=s3bucket,
                                    Body=output,
                                    Key='{}{}.json'.format(s3outputKey,id),
                                    Metadata = {'eventId': id },
                                    ContentType= 'application/json' )
        

def lambda_handler(event, context):
    print(event)
    eventid= event[EVENT][ID]    
    output= json.dumps(event,indent=4) 

    storeToS3(eventid,output)

    return {
        'statusCode': 200,
        'response': "End"
    }
