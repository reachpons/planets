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
    dynamoDBRegion = store['dynamoDB/region']
    
    client = bto.client('dynamodb', region_name=dynamoDBRegion)
    response = client.scan( TableName=dynamoDBTable,
                            ProjectionExpression='#_imageKey',
                            FilterExpression='#_eventId = :id',
                            ExpressionAttributeNames = {
                                    '#_eventId': 'eventId',
                                    '#_imageKey' : 'imageKey'
                            },
                            ExpressionAttributeValues={
                                    ':id': {'S': key}
                            } 
                        )
         
    
    return response['Items']

def getSignedUrl(eventId):
    
    rows=getEventDetail(eventId)
    imageKeys = [row['imageKey']['S'] for row in rows ]    
    distinctKeys=set(imageKeys)    

    s3Client = bto.client('s3')
    s3bucket = store['s3/bucket']
    urls=[]
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
        'body': json.dumps({ 'event': eventId,
                            'urls' : urls 
                            } )
    }