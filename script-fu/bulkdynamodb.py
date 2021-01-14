import json
import boto3 as bto

dynamodb = bto.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('alcolizer-dev-alcolizer-location-map')    

with open('alcolizer-dev-alcolizer-locations.json', 'r') as myfile:
    data=myfile.read()

# parse file
objects = json.loads(data)
print(objects)
#instance_id and cluster_id is the Key in dynamodb table 

for row in objects:
    
    table.put_item(Item=row)

    print (row)
