import boto3 as bto
import logging
import json
import sys
import uuid
from botocore.config import Config
from datetime import datetime
import os
from ssm_parameter_store import SSMParameterStore

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def search(bucket,imageKey,collectionId,logger):
    threshold = 85
    maxFaces=5

    try:
        
        config = Config(
            retries = dict(
                max_attempts = 10
            )
        )
        
        client=bto.client('rekognition',config=config)
        response=client.search_faces_by_image(CollectionId=collectionId,
                                    Image={'S3Object':{'Bucket':bucket,'Name':imageKey}},
                                    FaceMatchThreshold=threshold,
                                    MaxFaces=maxFaces)
    
                                    
        faceMatches=response['FaceMatches']
    except client.exceptions.InvalidParameterException as ie:
        logger.exception("Alcolizer-match-face - Invalid Exception for key %s. Implication is that there is no face in Image", imageKey )
        return None
        
    except Exception as e:
        logger.exception("Alcolizer-match-face - Rekognition Search by faces for key %s failed", imageKey )
        logger.exception(e) 
        raise  
    
    return faceMatches

def getTable():

    dynamoDBTable = store['dynamoDB/rekognition-result']
    dynamoDBRegion = store['dynamoDB/region']
    try:
        dynamodb = bto.resource('dynamodb', region_name=dynamoDBRegion)
        table = dynamodb.Table(dynamoDBTable)
        
    except:
        logger.exception("Could not connect to dbynamoDB table %s in region %s.", dynamoDBTable, dynamoDBRegion ) 
        sys.exit(1) 
    return table
    
def storeNoFacesToDynamonDB(eventid,key):
    rows=[]
    table=getTable()
    
    dateTimeIssued=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]    
    try:
        rowId=str(uuid.uuid1())
        row = {
                'rowUid' : rowId,
                'eventId' : eventid,
                'imageKey' : key,
                'utcSearchDatetime' : dateTimeIssued,
                'faceId' : '',
                'similarity': '',
                'externalImageId': ''
        }
        table.put_item(Item=row)
        rows.append(row)
        
    except exception as e:
        logger.exception(e) 
        raise  
        
    return rows
    
    
def storeToDynamonDB(eventid,key,results):
    rows=[]
    table=getTable()
    
    dateTimeIssued=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    for match in results:
        try:
            rowId=str(uuid.uuid1())
            row = {
                    'rowUid' : rowId,
                    'eventId' : eventid,
                    'imageKey' : key,
                    'faceId' : match['Face']['FaceId'],
                    'similarity': str(match['Similarity']),
                    'utcSearchDatetime' : dateTimeIssued,
                    'externalImageId': match['Face']['ExternalImageId']
            }
            table.put_item(Item=row)
            rows.append(row)
            
        except exception as e:
            logger.exception(e) 
            raise  
        
    return rows
 
def lambda_handler(event,context):
    
    global logger
    logger=establish_logger()
    logger.info(event) 

    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )
    
    collectionId = store['collection-id']
    bucket = store['s3/bucket']
    
    eventid=event['event-id']
    
    s3 = bto.client('s3')    
    key = event['image']['imagekey']
        
    logger.info("New file [%s] added to the s3 Bucket [%s].",key,bucket)

    matches=search(bucket,key,collectionId,logger)
    faces=[]
    
    if not matches: 
        faces=storeNoFacesToDynamonDB(eventid,key)
    else:
        faces = storeToDynamonDB(eventid,key,matches)
    
    
    return {  
            'match' :  {
                'imagekey' : key,
                'statusCode': 200,
                'event': { 'id': eventid } , 
                'matchedFaces' : faces
            }
    }