import logging
import json
import boto3 as bto
import json
from ssm_parameter_store import SSMParameterStore
from boto3.dynamodb.conditions import Key


def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr


def getSignedURL(s3Client, bucket,key):
    
    #print(quote(key))
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
        urls.append( getSignedURL(s3Client,s3bucket,key)  )

    return urls

def main():

    global logger
    logger=establish_logger()
    
    hierarchy = 'dev' #os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    urls=getSignedUrl('12793428-3929-11eb-92b4-0338ba2a47cb') #06b8d24c-351b-11eb-b511-b315bfe046f8')    
    
    print( json.dumps( {'urls' : urls }, indent=4 ))

if __name__ == "__main__":
    main()