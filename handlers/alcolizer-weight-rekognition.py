import json
import logging

EVENT='event'
ID='id'
ALCOLIZER_RESULTS='alcolizerResults'
RESULT_DISPLAY_TEXT='resultDisplayedText'
MATCHES='matches'
MATCH='match'
IMAGEKEY='imagekey'
MATCHED_FACES='matchedFaces'
EXTERNAL_IMAGE_ID='externalImageId'
SIMILARITY='similarity'

def establish_logger():
    logr = logging.getLogger()
    logr.setLevel(logging.INFO)
    return logr
    
def lambda_handler(event, context):
    
    logger=establish_logger()
    logger.info(event) 

    pair=[]
    answer=None
    similarity,sapid='0.0',''
    
    for item in event:
        match=item[MATCH]
        for face in match[MATCHED_FACES]:
            pair.append(( face[SIMILARITY],face[EXTERNAL_IMAGE_ID] ) )

    pair.sort(reverse=True, key = lambda x: x[0])  

    if pair:
        answer=pair[0]

    print('\n'.join('{}: {}'.format(*k) for k in enumerate(pair)))
    
    if answer is not None:
        similarity,sapid =answer[0], answer[1]
    
    return {
        'weightedOutcome' : {
            "similarity" : similarity,
            "sapid" :sapid
        }
    }