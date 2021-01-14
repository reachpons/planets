import boto3


PARAMETERS ='Parameters'

class SSMParameterStore(object):

    def __init__(self, SSM_Client=None, Path=None, Encryption=False):
        self._path = (Path or '').rstrip('/') + '/'
        self._client = SSM_Client or boto3.client('ssm')
        self._max=10
        self._encryption=Encryption
        self._params={}
        self.getParametersByPath()
    
    def getParametersByPath(self):        
        response = self._client.get_parameters_by_path(Path=self._path, Recursive=True, MaxResults=self._max, WithDecryption=self._encryption)        
        while response:            
            parameters = response[PARAMETERS]  
            self.extract(parameters)
            if 'NextToken' not in response: break    
            nextToken=response.get('NextToken') 
            response = self._client.get_parameters_by_path(Path=self._path, Recursive=True, MaxResults=self._max, WithDecryption=self._encryption, NextToken=nextToken)            

        return self._params
    
    def extract(self,parameters):
        for p in parameters:   
            key = str(p['Name'])[len(self._path):] 
            value=str(p['Value'])        
            self._params[key]=value

    def __getitem__(self, name):
        return self._params.get(name)

    def __setitem__(self, key, value):
        raise NotImplementedError()
    
    def __delitem__(self, name):
        raise NotImplementedError