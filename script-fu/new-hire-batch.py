import boto3 as bto
import json
import logging



def openGallagher(fileName):
    with open(fileName) as f:
        readf = json.load(f)
    return readf

def openRekognition(fileName):
    with open(fileName) as f:
        readf = json.load(f)
    return readf

def main():
   
    gallagher=openGallagher('cardholders.json')
    cardholders=gallagher.keys()
    
    collection=openRekognition('collection-sapids.json')       
    saps=collection.keys()
   
    ans=cardholders-saps
    print(len(cardholders))
    print(len(saps))
    print(len(ans))
    print(ans)
    
if __name__ == "__main__":
    main()
