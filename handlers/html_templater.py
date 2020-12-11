import io
import boto3 as bto
import json
from string import Template 
from urllib.parse import unquote

class Templater(object):

    def __init__(self, Bucket= None, Template = None):
        self._s3TemplateKey=Template
        self._s3Bucket=Bucket
        self._content=None
        self.getTemplate()
    
    def getTemplate(self):        
        s3 = bto.resource('s3')    
        bytes_buffer = io.BytesIO()

        unkey = unquote(self._s3TemplateKey)        
        obj = s3.Object(self._s3Bucket, unkey)        
        
        self._content = obj.get()['Body'].read().decode('utf-8')        

    def combine(self,data):
        plate = Template(self._content)
        body=plate.substitute(data)
        return body


    