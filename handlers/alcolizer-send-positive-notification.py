import boto3 as bto
import json
import logging

EVENT='event'
ALCOLIZER_RESULT='alcolizerResult'
ALCOHOL='internalValue'

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr

def lambda_handler(event, context):

    global logger
    logger=establish_logger()
       
   
    # Evaluate  the type of email from the content  
    # to be completed at a later date

    alcohol = event[EVENT][ALCOLIZER_RESULT][ALCOHOL]

    return {
        'manager': 'ibunney@fmgl.com.au',
        'alcohol' : alcohol
    }
