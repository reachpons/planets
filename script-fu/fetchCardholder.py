import boto3 as bto
import urllib3
import json
import sys
import imghdr 
from datetime import datetime
from ssm_parameter_store import SSMParameterStore
from gallagher_api import GallagherConnection
import base64


def add_faces_to_collection(blob,externalImageId,collectionId):    

    client=bto.client('rekognition')    
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
    collectionId = store['collection-id']
    for sapid in full_db.keys():
        hire=full_db.get(sapid)
        if hire is not None:    
            gallagherId=hire['id']  # get unique gallagher Identifier
            count+=1
            print('{}--{}'.format(count,hire))
            data=gallagher.getPhoto(gallagherId) 
            if data is not None :                           
                add_faces_to_collection(data,str(sapid),collectionId)                      

def main():
   
    hierarchy = 'dev' # os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    gallagherAPIUrl = store['gallagher/API-url']
    authorizationKey=store['gallagher/authorizationKey']
    gallagher=GallagherConnection(gallagherAPIUrl,authorizationKey)

    print("Start fetch from Gallagher")
    full_db=gallagher.getGallagherCardholders()
    
    #with open('cardholders.json', 'w') as f:
    #    json.dump(full_db, f, indent=4)

    print("Start adding to collection")
    putNewHires(gallagher,full_db)



if __name__ == "__main__":
    print( "Start Time {0}".format(datetime.utcnow().strftime("%H:%M:%S")))
    main()
    print( "Finish End {0}".format(datetime.utcnow().strftime("%H:%M:%S")) )