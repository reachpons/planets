#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)
from datetime import datetime
import boto3

def main():

    collectionId='uat-rekognition-collection'
    fileName='output/singlefile-517547.jpg'
    threshold = 90
    maxFaces=5

    with open(fileName, mode='rb') as file: # b is important -> binary
        fileContent = file.read()
    
    client=boto3.client('rekognition')

    response=client.search_faces_by_image(CollectionId=collectionId,
                                 Image={  "Bytes" : fileContent },
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)

                                
    faceMatches=response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print


if __name__ == "__main__":
    print( "Start Time {0}".format(datetime.utcnow().strftime("%H:%M:%S")))
    main()
    print( "Finish End {0}".format(datetime.utcnow().strftime("%H:%M:%S")) )