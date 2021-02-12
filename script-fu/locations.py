import json
import boto3 as bto
from boto3.dynamodb.conditions import Key, Attr

class Location(object):

    def __init__(self, store):
        self._table=table= store['dynamoDB/location']
        self._region = store['dynamoDB/region']
        self._default = store['location/default']
    

    def __getitem__(self, key):
        return self.fetch(key)

    def __setitem__(self, key, value):
        raise NotImplementedError()
    
    def __delitem__(self, name):
        raise NotImplementedError()

    def fetch(self,key):                
        
        client = bto.resource('dynamodb', region_name=self._region)        
        table=client.Table(self._table)
        response = table.query( 
                            KeyConditionExpression=Key('serialNo').eq(key)
                            )
        return response['Items'][0] if response['Items'] else None
    
    def parse(self,results):
    
        if (results):
            return  results['location'], results['site']                    

        return self._default.split(':')[1], self._default.split(':')[0]

    def isBlocked(self,results):
    
        if (results):
            return  results['isBlocked']

        return True
