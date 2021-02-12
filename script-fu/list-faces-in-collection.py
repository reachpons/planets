
import json
import boto3
from datetime import datetime

def list_faces_in_collection(collection_id):
   
    maxResults=4096

    client=boto3.client('rekognition')
    
    all={}
    cycle=0
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)
    while response:

        faces=response['Faces']
        for face in faces:
            all[face['ExternalImageId']]=face['FaceId']
            faces_count+=1
        
        if 'NextToken' not in response: break           
        response=client.list_faces(CollectionId=collection_id,
                                    MaxResults=maxResults,
                                    NextToken=response['NextToken'])     
       

    return all   

def main():

    print(datetime.utcnow())
    collection_id='large-rekognition-collection'

    saps=list_faces_in_collection(collection_id)
    print( "faces count: {}".format(len(saps)) )

    print(datetime.utcnow())

if __name__ == "__main__":
    main()