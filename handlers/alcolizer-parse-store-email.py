import boto3 as bto
import base64
import json
import uuid
from datetime import datetime
import logging
import os
from ssm_parameter_store import SSMParameterStore
from urllib.parse import unquote


def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def loadEmail(s3bucket,s3key):
    s3 = bto.resource('s3')
    
    unkey = unquote(s3key)
    obj = s3.Object(s3bucket, unkey)
    
    body = obj.get()['Body'].read()
    return json.loads(body)

def parseIdentification(dict,data):
    if dict is None: return
    data['serialNo']=dict.get('serial')['value']
    data['software']=dict.get('software')['value']
    data['assembly']=dict.get('assembly')['value']

      
def storeToDynamoDB(row):
    dynamoDBTable = store['dynamoDB/breathalyzer-result-table']
    dynamoDBRegion = store['dynamoDB/region']
    try:
        dynamodb = bto.resource('dynamodb', region_name=dynamoDBRegion)
        table = dynamodb.Table(dynamoDBTable)    

    except:
        logger.exception("Could not connect to dbynamoDB table %s in region %s.", dynamoDBTable, dynamoDBRegion ) 
        sys.exit(1) 
    
    table.put_item(Item=row)

def saveImages(images,eventId):
    s3bucket = store['s3/bucket']

    for img in images:  
        message_bytes = base64.b64decode(img["raw"])
        s3Client = bto.client('s3')
        response = s3Client.put_object( Bucket=s3bucket,
                                        Body=message_bytes,
                                        Key=img["imagekey"],
                                        Metadata = {'eventId': eventId },
                                        ContentType= 'image/jpeg' )
                                        
def splitEmail(content):
    # 1 - LogRecordID
    # 2 - TitleOfLog
    # 3 - Alcolizer created timestamp 
    # 47 - photo
    # 54 - Result (Range)
    # 9 - Result (Dislayed)
    # 5 - Internal Raw EXact
    # 55 - Result (Alcohol Detected)
    # 56 - Result
    
    records=(content['records'])
    photos=[]
    data={}
    images=[]

    s3FacesKey = store['s3/facesKey']
    eventid=str(uuid.uuid1())
    utcDateIssued=datetime.utcnow()
    
    for itm in records[0]:    
        ix='{}year={}/month={}/day={}/{}.jpg'.format(s3FacesKey,utcDateIssued.year,utcDateIssued.month,utcDateIssued.day,str(uuid.uuid1()))            
        if itm['id'] == '1': 
            data['logRecordID']=itm["raw"]
            data['eventId']= eventid
        data['utcdatetime'] =datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]    
        if itm['id'] == '3': data['alcolizerDateTime']=itm["ui_text"]
        if itm['id'] == '47': photos.append({ 'imagekey' : ix , 'raw' : itm["raw"] })
        if itm['id'] == '5': 
            data['internalRaw']= itm["raw"]
            data['internalValue']= itm["value"]
            data['internalText']= itm["ui_text"]            
        if itm['id'] == '54': 
            data['resultRange']=itm["raw"]
            data['resultRangeText']=itm["ui_text"]            
        if itm['id'] == '9': 
            data['resultDisplayed']=itm["raw"]
            data['resultDisplayedText']=itm["ui_text"]
        if itm['id'] == '55': 
            data['resultAlcohol']=itm["raw"]
            data['resultAlcoholText']=itm["ui_text"]
        if itm['id'] == '56': 
            data['result']=itm["raw"]
            data['resultText']=itm["ui_text"]
    
    for img in photos: 
        images.append({ 'imagekey': img["imagekey"] })
        
    data['version']=content.get('version')
    parseIdentification(content.get('identification'),data)

    storeToDynamoDB(data)
    saveImages(photos, data['eventId'])
    
    return {'statusCode': 200,
            'event': {
                    'id' : eventid , 
                    'images' : images,
                    'alcolizerResult'  : data
            }
    }

def lambda_handler(event, context):
      
    global logger
    logger=establish_logger()
    
    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    bucket = event['email']['bucket']
    key = event['email']['key']
    
    content=loadEmail(bucket,key)
    
    return splitEmail(content)