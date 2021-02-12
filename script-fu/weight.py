import json
from os import listdir
from os.path import isfile, join

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


def determine(pairs):
    
    confidence='Maximum' if pairs else "Uncertain"
    final,sim,sapid=0.00,0.00,''

    if pairs:
        answer=pairs[0]

        # if no sapid => there was no faces identified
        if not answer[1]: return (sapid,final,'None')
        final,sim,sapid =float(answer[0]), float(answer[0]), answer[1]
        
        # IF similarity > 99 
        # THEN we have positive ID and can stop further processing
        if sim < 99:
             # IF second highest similarity is SAME ID  &  Addition law of probability > 99
            # THEN Stop further processing  

            # P = P(A) and P(B) - P(A or B)

            answer=pairs[1]  
            if not answer[1]: return (sapid,final,'Single')   
            sim1,sapid1 =float(answer[0]), answer[1]                       

            if sapid==sapid1:                
                final = ((sim/100)+(sim1/100)-((sim/100)*(sim1/100)))*100
                confidence='High' if final > 99 else 'Low'                
            else:
                confidence='Uncertain'

    return (sapid,final,confidence)

def weight(event):
    pairs=[]
    answer=None
    similarity,sapid='0.0',''

    for item in event:
        match=item[MATCH]
        for face in match[MATCHED_FACES]:
            pairs.append(( face[SIMILARITY],face[EXTERNAL_IMAGE_ID] ) )

    pairs.sort(reverse=True, key = lambda x: x[0])  
 

    sapid,final,confidence=determine(pairs)
           
    return { 
        'weightedOutcome' : {
            'similarity' : final,
            'sapid' :sapid,
            'confidence' : confidence
        }
    }
        

def main():
    
    mypath='output/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #print(onlyfiles)
  
    for name in onlyfiles:
        with open('output/{}'.format(name)) as f:
            dict = json.load(f)       
            
            ans = { 
                'eventid' : dict[EVENT][ID],
                'weight' : weight(dict[EVENT])
            }
            print( json.dumps(ans,indent=4 ) )
        


if __name__ == '__main__':
    main()


