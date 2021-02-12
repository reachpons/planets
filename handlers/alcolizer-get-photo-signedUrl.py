import logging
import json
import boto3 as bto
import json
import os
from ssm_parameter_store import SSMParameterStore
from boto3.dynamodb.conditions import Key


def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def getURL(s3Client, bucket,key):        
    url = s3Client.generate_presigned_url(ClientMethod='get_object',ExpiresIn=3600, Params= {'Bucket':bucket,'Key': key } )
    return url

def getEventDetail(key):

    dynamoDBTable = store['dynamoDB/rekognition-result']
    index = store['dynamoDB/rekognition-result-secondary-index']
    dynamoDBRegion = store['dynamoDB/region']
    
    client = bto.resource('dynamodb', region_name=dynamoDBRegion)
    table=client.Table(dynamoDBTable)
        
    response = table.query( IndexName=index,
                            KeyConditionExpression=Key('eventId').eq(key)
                        )
    logger.info(response)
    return response['Items'] 


def getSignedUrl(eventId):
    
    urls=[]
    
    rows=getEventDetail(eventId)    
    if rows:
        imageKeys = [row['imageKey'] for row in rows ]    
        distinctKeys=set(imageKeys)    
    
        s3Client = bto.client('s3')
        s3bucket = store['s3/bucket']
        for key in distinctKeys:
            urls.append( getURL(s3Client,s3bucket,key)  )

    return urls


def lambda_handler(event, context):

    global logger
    logger=establish_logger()

    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    eventId=event['pathParameters']['event']
    
    urls=getSignedUrl(eventId)    

    return {
        'statusCode': 200,
        'headers': { 
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps({ 'event': eventId,
                            'urls' : urls 
                            } )
    }