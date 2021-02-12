import json
import logging
import os
import boto3 as bto
from ssm_parameter_store import SSMParameterStore



def main():

    hierarchy = 'dev'
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )        

    blocked = store['notification/blocked']

    print(blocked=='True')

if __name__ == "__main__":
    main()
