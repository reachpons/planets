import json
import boto3

def getParameter(name):
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name=name, WithDecryption=False)['Parameter']
    return parameter['Value']

def lambda_handler(event, context):
    
    stepARN = getParameter('/alcolizer-rekognition/step-function')
    client = boto3.client('stepfunctions')
    
    response = client.start_execution (
            stateMachineArn=stepARN,
            input=json.dumps(event)
            )

    return {
        'statusCode': 200,
        'response': "Started"
    }