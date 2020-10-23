import json
import boto3
import os
from ssm_parameter_store import SSMParameterStore

def lambda_handler(event, context):
    
    hierarchy = os.environ['hierarchy']
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )
    
    stepARN =store['step-function']

    client = boto3.client('stepfunctions')
    
    response = client.start_execution (stateMachineArn = stepARN, input = json.dumps(event) )

    return {
        'statusCode': 200,
        'response': "Started"
    }