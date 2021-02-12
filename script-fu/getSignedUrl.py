import json
import boto3 as bto
import urllib3
import json
from urllib.parse import quote

def listy():

    s3 = bto.resource('s3')
    s3_client = bto.client('s3')

    #Your Bucket Name
    bucket = s3.Bucket('dev-alcolizer-rekognition')

    #Gets the list of objects in the Bucket
    s3_Bucket_iterator = bucket.objects.all()

    #Generates the Signed URL for each object in the Bucket 
    for i in s3_Bucket_iterator:
        #url = s3_client.generate_presigned_url(ClientMethod='get_object',Params={'Bucket':bucket.name,'Key':i.key})
        print(i.key)


def getSignedURL(s3Client, bucket,key):
    
    #print(quote(key))
    url = s3Client.generate_presigned_url(ClientMethod='get_object',ExpiresIn=3600, Params= {'Bucket':bucket,'Key': key } )
    return url


def main():

    bucket='dev-alcolizer-rekognition'
    key='faces/year=2020/month=12/day=3/0d070347-351b-11eb-b5ad-b315bfe046f8.jpg'
        
    s3Client = bto.client('s3')

    #print(quote(key))
    url =getSignedURL(s3Client,bucket,key)    

    print(url)



if __name__ == "__main__":
    main()


