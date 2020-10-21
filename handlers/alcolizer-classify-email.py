import json
from enum import Enum

class category(Enum):
    BREATH_TEST =1
    CALIBRATION_LOG=2
    ALCOLIZER_ALERT=3

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Evaluate  the type of email from the content  
    # to be completed at a later date

    outcome="isBreathTest"

    # outcome="isDailyCalibrationLog"
    # outcome="isAlcolyzerAlert"

    return {
        'statusCode': 200,
        'category': outcome,
        'email' : {
            'bucket' : bucket,
            'key' : key
        }
    }
