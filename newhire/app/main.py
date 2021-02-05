import boto3 as bto
import urllib3
import json
import sys
import imghdr 
from datetime import datetime
from ssm_parameter_store import SSMParameterStore
from gallagher_api import GallagherConnection
import base64
import os


def add_faces_to_collection(blob,externalImageId,collectionId):    
    client=bto.client('rekognition', region_name='ap-southeast-2')    
    response=client.index_faces(CollectionId=collectionId,
                                Image={  "Bytes" : blob },
                                ExternalImageId=externalImageId,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])
    return len(response['FaceRecords'])


def writeImage(message_bytes,id):    
    with open('output/singlefile-{}.jpg'.format(id), "wb") as file:
        file.write(message_bytes)      

def putNewHires(gallagher,full_db):
    count=0
    collectionId = store['rekognition/collection-id']
    for sapid in full_db.keys():
        hire=full_db.get(sapid)
        if hire is not None:    
            gallagherId=hire['id']  # get unique gallagher Identifier
            count+=1
            print('{}--{}'.format(count,hire))
            data=gallagher.getPhoto(gallagherId) 
            if data is not None :                           
                add_faces_to_collection(data,str(sapid),collectionId)                     

def IdentifyNewHire(full_db,collectionId):
    # Identify the faces in Facial rekognition collection.
    maxResults=4096
    client=bto.client('rekognition', region_name='ap-southeast-2')     
    collresponse=client.list_faces(CollectionId=collectionId,MaxResults=maxResults)
    # Set that holds all the SAPIDs from AWS Facial rekognition Collection
    fullrekcollec=set() 
    while collresponse:
        Subrekog =set(sub['ExternalImageId'] for sub in collresponse['Faces'])
        fullrekcollec.update(Subrekog)
        if 'NextToken' not in collresponse: break 
        collresponse=client.list_faces(CollectionId=collectionId,
                                    MaxResults=maxResults,
                                    NextToken=collresponse['NextToken']) 
    #Set that holds all the SAPIDs from Gallagher application.
    FromGallagher = set(str(sapid) for sapid in full_db.keys()) 
    # Identify new hire collection
    Newhire=FromGallagher-fullrekcollec  
    NewhireDataset =dict()
    for (key,value) in full_db.items():
        if str(key) in Newhire:
            NewhireDataset[key]= value
    print(" Total number of records from Gallagher :"+str(len(FromGallagher)))
    print(" Total number of records from Rekognition :"+str(len(fullrekcollec)))
    print(" Total number of people not in Rekognition but in Gallagher :"+str(len(Newhire)))
    return NewhireDataset


def main():
    client=bto.client('rekognition')
    hierarchy = os.environ['env_prefix']
    # hierarchy = 'dev'
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )
    collectionId = store['rekognition/collection-id']
    print(collectionId)
    # Check and create new collection if already not-exist
    listresponse=client.list_collections(MaxResults=20)
    if collectionId in listresponse['CollectionIds']:
        print('Collection already exist')
    else:
        print('Collection not exist... So creating new facial rekognition collection')
        createresponse=client.create_collection(CollectionId=collection_id)
        print('Collection ARN: ' + createresponse['CollectionArn'])
        print('Status code: ' + str(createresponse['StatusCode']))
        print('Done...')
    gallagherAPIUrl = store['gallagher/API-url']
    authorizationKey=store['gallagher/authorizationKey']
    gallagher=GallagherConnection(gallagherAPIUrl,authorizationKey)

    print("Start fetch from Gallagher")
    full_db=gallagher.getGallagherCardholders()
    
    print("Identify the new person that needs to be added into collection")
    NewHire=IdentifyNewHire(full_db,collectionId)

    print("Start adding to collection")
    putNewHires(gallagher,NewHire)
if __name__ == "__main__":
    print( "Start Time {0}".format(datetime.utcnow().strftime("%H:%M:%S")))
    main()
    print( "Finish End {0}".format(datetime.utcnow().strftime("%H:%M:%S")) )