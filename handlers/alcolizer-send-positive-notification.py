import json
import logging
import os
from string import Template 
from html_templater import Templater
from ssm_parameter_store import SSMParameterStore


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

    hierarchy = os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )

    s3bucket = store['s3/bucket']
    htmltemplate=store['s3/email/html-template']

    #
    # Insert API Call to get Personel & Supervisor details Here
    #

    # Dummy data set
    data= {
            'surname' : 'Jackson',
            'givenNames' :'Andrew Micheal',
            'shift' :'Day',
            'department' : 'TPI Rail',
            'company' : 'Verve Group',
            'supervisorSurname' :'Windsor', 
            'supervisorGivenNames' :'Philip',
            'datetime' : '8 August 2020:6:30 AM',
            'alcolizer' :'33000695',
            'displayedResult' : '0.005 g/100mL BAC'
        }

    templater=Templater(Bucket=s3bucket,Template= htmltemplate )
    body=templater.combine(data)

    #
    # Insert API call to send email here
    # Fan out ? push onto SNS Topic ?
    # 

    return {
        'manager': '<feature not yet implemented>',
        'alcohol' : alcohol 
    }

