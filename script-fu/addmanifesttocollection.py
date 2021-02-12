import json 
import boto3

def add_faces_to_collection(bucket,photo,collection_id,externalImageId):
    client=boto3.client('rekognition')    
    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=externalImageId,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])
    
    return len(response['FaceRecords'])

def sapID(s3Key):
    if(len(s3Key.split("/")[-1])):
        jpg=s3Key.split("-")[-1]
        sapid=jpg.split(".")[0]
        return sapid
    return None

def main():
    collectionId="large-rekognition-collection"
    s3Bucket="large-alcolizer-rekognition"    
    count=0
    with open("manifest/a28e22c0-31ee-49ee-b41b-f67596559884.csv") as fp: 
        for line in fp: 
            count += 1
            s3Key= line.split(",")[-1].replace("\"","").strip()
            sap=sapID(s3Key)       
            print("Line -> {}: SAP Id-> {} Name -> {} ".format(count, sap, s3Key)) 
            add_faces_to_collection(s3Bucket,s3Key,collectionId,sap)

if __name__ == "__main__":
    main()    
