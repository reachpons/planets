import boto3 as bto
import json
import logging
from ssm_parameter_store import SSMParameterStore


def main():
        
    hierarchy='dev'
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )



if __name__ == '__main__':
    main()


