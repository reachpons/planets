import boto3 as bto
import json
import logging
import os
from urllib.parse import unquote
from locations import Location
from ssm_parameter_store import SSMParameterStore

# The Alcolizer sends 3 different email attachments  (in JSON format)
# Status = usually and Alcolizer notification like liquid detected , service required
# Log = daily Log of the machine activity 
# Result = Individual Test Result
#
# All have the 'indentification' element
#
# Only Status has the 'groups' and 'set' json elements
# Both the Log & Result have 'records' & 'parameters' json elements
# Only Log have paramaters with 'id' = 22, 23  
# Only Result  have paramaters with 'id' = 47, 56, 54, 9, 2

GROUPS ='groups'
SET ='set'
PARAMETERS='parameters'
RECORDS='records'
EMAIL='email'
BUCKET='bucket'
KEY='key'

IS_BREATH='isBreathTest'
IS_STATUS='isStatusReport'
IS_LOG='isLogReport'
IS_UNKOWN='isUnkown'
IS_NULL='isNullAttachment'

STATUS='statusCode'
CATEGORY='category'
NOTE='note'
IS_BLOCKED='isBlocked'

def loadAttachment(s3bucket,s3key):
    s3 = bto.resource('s3')
    
    unkey = unquote(s3key)
    
    obj = s3.Object(s3bucket, unkey)

    body = obj.get()['Body'].read()
    return json.loads(body)


def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def isStatus(dict):
    if dict is None: return None

    groupsEle=dict.get(GROUPS)
    setEle=dict.get(SET)

    return groupsEle is not None and setEle is not None

def isLog(dict):
    
    params=dict.get(PARAMETERS)  
    if params is None : return False 
    
    return {'22','23'} <= params.keys()

def isResult(dict):
    
    params=dict.get(PARAMETERS)   
    if params is None : return False 

    #test whether every element in l in r 
    return  {'47','56','54','9','2'} <= params.keys()

def unrecognisedIgnore(dict):

    return false

def parseIdentification(dict):

    data={}
    if dict is None: return
    data['serialNo']=dict.get('serial')['value']
    data['software']=dict.get('software')['value']
    data['assembly']=dict.get('assembly')['value']

    return data

def statusReport(dict):
    if dict is None: return None

    groups=dict.get(GROUPS)
    sets=dict.get(SET)
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

def logReport(dict):
    if dict is None: return None

    records=dict.get(RECORDS)
    parameters=dict[PARAMETERS]
    rslts=[]
    for rec in records:
        for itm in rec:
            param=parameters[itm['id']]
            rs={
                'ui-text' : itm['ui_text'],
                'raw-text' : itm['raw'],            
                'title' : param['ui_title'],
                'decription' : param['ui_description']
            }
            rslts.append(rs)

            
    report = {
        RECORDS :rslts
    }
    return report

def isAlcolizerBlocked(content,category):
    
    if category != IS_BREATH: return False

    records=(content['records'])
    idData=parseIdentification(content.get('identification'))
    
    location= Location(store)
    results=location[int(idData['serialNo'])]

    return location.isBlocked(results)

def parseAttachment(attachment):
          
    if isResult(attachment):              
        category,reportType=IS_BREATH,"Breathalyser Report"
    elif isStatus(attachment):
        category,reportType=IS_STATUS,"Status Report"
    elif isLog(attachment):         
        category,reportType=IS_LOG,"Log Report"
    else:
        category,reportType=IS_UNKOWN,'Unknown email Attachment Type'

    return category,reportType 


def lambda_handler(event, context):

    global logger
    logger=establish_logger()
        
    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )
       
    bucket = event[EMAIL][ BUCKET ]
    key = event[EMAIL][KEY]
    
    
    if key is not None:
        content=loadAttachment(bucket,key)
        category,reportType= parseAttachment(content)
    else:
        category,reportType=IS_NULL,'No Attachment'

    blocked = isAlcolizerBlocked(content,category)

    return {
            STATUS: 200,
            CATEGORY: category, 
            NOTE  : reportType,
            IS_BLOCKED : blocked,         
            EMAIL : {
                    BUCKET : bucket,
                    KEY : key
                }
        }          
