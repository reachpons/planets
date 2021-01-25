import boto3 as bto
import json
import logging
import os

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr


def lambda_handler(event, context):

    global logger
    logger=establish_logger()

    hierarchy = os.environ['hierarchy']
    global store
    #store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )


    #
    # Insert API call to send email here
    # Fan out ? push onto SNS Topic ?
    # 

    return {
        'manager': '<feature not yet implemented>'
    }

