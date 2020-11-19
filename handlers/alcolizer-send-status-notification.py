import boto3 as bto
import json
import logging

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr


def lambda_handler(event, context):

    global logger
    logger=establish_logger()

    
    # Evaluate  the type of email from the content  
    # to be completed at a later date

    return {
        'status': 'report'
    }
