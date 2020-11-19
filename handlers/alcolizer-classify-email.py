import boto3 as bto
import json
import logging
from urllib.parse import unquote

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

    groupsEle=dict.get('groups')
    setEle=dict.get('set')

    return groupsEle is not None and setEle is not None

def isLog(dict):
    
    params=dict.get('parameters')  
    return {'22','23'} <= params.keys()

def isResult(dict):
    
    params=dict.get('parameters')   
    if params is None : return False 

    #test whether every element in l in r 
    return  {'47','56','54','9','2'} <= params.keys()

def unrecognisedIgnore(dict):

    return false

def statusReport(dict):
    if dict is None: return None

    groups=dict.get('groups')
    sets=dict.get('set')
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

    records=dict.get('records')
    parameters=dict['parameters']
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
        'records' :rslts
    }
    return report


def parseAttachment(attachment):
          
    if isResult(attachment):         
        category,reportType="isBreathTest","Breathalyser Report"
    elif isStatus(attachment):
        category,reportType="isStatusReport","Status Report"
    elif isLog(attachment):         
        category,reportType="isLogReport","Log Report"
    else:
        category,reportType="isUnkown",'Unknown email Attachment Type'

    return category,reportType 


def lambda_handler(event, context):

    global logger
    logger=establish_logger()
       
    bucket = event['email']['bucket']
    key = event['email']['key']
    
    # Evaluate  the type of email from the content  
    # to be completed at a later date

    content=loadAttachment(bucket,key)

    category,reportType= parseAttachment(content)

    return {
            'statusCode': 200,
            'category': category, 
            'note'  : reportType,         
            'email' : {
                    'bucket' : bucket,
                    'key' : key
                }
        }          
