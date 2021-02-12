import boto3 as bto
import json
import logging
import email
import uuid
import logging
from urllib.parse import unquote
from ssm_parameter_store import SSMParameterStore
from datetime import datetime


def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def loadfile(s3bucket,s3key):
    s3 = bto.resource('s3')
    
    unkey = unquote(s3key)
    obj = s3.Object(s3bucket, unkey)
    
    body = obj.get()['Body'].read()
    return body

def isJSON(content):
  try:
    json_object = json.loads(content)
  except ValueError as e:
    return False
  return True

def chevronLess(whole):
    rslt=whole[whole.find('<')+1 : whole.rfind('>')]
    return rslt

def storeToS3(output,partName):
    
    attachmentId=str(uuid.uuid1())

    suffix=partName.split('.')[0]
    s3bucket = store['s3/bucket']
    s3outputKey = store['s3/attachmentKey']
    
    utcDateIssued=datetime.utcnow()   
    ix='{}year={}/month={}/day={}/{}-{}.json'.format(s3outputKey,utcDateIssued.year,utcDateIssued.month,utcDateIssued.day,suffix,attachmentId)
    #ix='{}{}-{}.json'.format(s3outputKey,suffix,attachmentId)

    s3Client = bto.client('s3')
    response = s3Client.put_object( Bucket=s3bucket,
                                    Body=output,
                                    Key=ix,
                                    ContentType= 'application/json',
                                    ACL='bucket-owner-full-control' )

def getAttachment(content):
    
    #content = readLocal(filename)
    
    decoded = content.decode('utf-8') #utf-8
    #print(decoded)
    msg = email.message_from_string(decoded)  #encoding = 'ISO-8859-1'

    msg_content_type = msg.get_content_type()


    print('Return-Path->{}'.format(chevronLess(msg['Return-Path'])))
    print('Received->{}'.format(chevronLess(msg['Received'])))
    print('To->{}'.format(chevronLess(msg['To'])))
    print('From->{}'.format(chevronLess(msg['From'])))

    print('Return-Path->{}'.format(msg['Return-Path']))
    print('Received->{}'.format(msg['Received']))
    print('To->{}'.format(msg['To']))
    print('From->{}'.format(msg['From']))
    print('Subject->{}'.format(msg['Subject']))
    print('DKIM-Signature->{}'.format(msg['DKIM-Signature']))
    
    for part in msg.walk():

        if part.get_content_maintype() == 'multipart':            
            continue

        disposition=part.get('Content-Disposition')
        if disposition is None:
            continue

        partName=part.get_filename()
        partPay=part.get_payload(decode=True)
        if isJSON(partPay)  and '.json' in partName :
            #print( part['Content-Transfer-Encoding'] )
            print('{}\n{}\n{}'.format(partPay,disposition,partName)) 
            print ( partPay ) 
            #storeToS3(partPay,partName)

    return True


def main():
        
    global logger
    logger=establish_logger()
    
    #hierarchy = os.environ['hierarchy']
    hierarchy='dev'
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )


    key = 'raw/438u3hu7mn3rvei88airhtgu4708jur0cv5lipo1'
    bucket='large-alcolizer-rekognition'

    email=loadfile(bucket,key)

    rslt=getAttachment(email)



if __name__ == '__main__':
    main()


