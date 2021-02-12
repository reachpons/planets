import boto3 as bto
import json
import logging
from locations import Location
from ssm_parameter_store import SSMParameterStore

logger=None

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


def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def parseIdentification(dict):
    data={}
    if dict is None: return None

    data['serialNo']=dict.get('serial')['value']
    data['software']=dict.get('software')['value']
    data['assembly']=dict.get('assembly')['value']
    return data

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

def isAlcolizerBlocked(content):
    
    records=(content['records'])
    idData=parseIdentification(content.get('identification'))
    
    location= Location(store)
    results=location[int(idData['serialNo'])]
    return location.isBlocked(results)

def parseIdentification(dict):

    data={}
    if dict is None: return
    data['serialNo']=dict.get('serial')['value']
    data['software']=dict.get('software')['value']
    data['assembly']=dict.get('assembly')['value']

    return data

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


def readAttachment(fileName):
    with open(fileName) as f:
        readf = json.load(f)
    return readf

def main():

    bucket='bucket'
    key='key'

    filename='result-attachment.json'
    
    hierarchy = 'dev'
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    #logger=establish_logger()
    attachment=readAttachment(filename)
   

    
    blocked= isAlcolizerBlocked(attachment)

    print(blocked)
    return 

    thing= {
            'statusCode': 200,
            'category': catagory,
            'Alcolizer' : machine,
            reportType : content     
        }             
    print(json.dumps(thing, indent=4))

if __name__ == "__main__":
    main()
