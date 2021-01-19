
import json
import boto3 as bto


def getConfigDataFromFile():
    with open('notification-rule-config.json', 'r') as myfile:
        data=myfile.read()
    return json.loads(data)

def main():

    value = getConfigDataFromFile()

    # parse file
    pretty =json.dumps(value,indent=4)

    ssm = bto.client('ssm')

    response = ssm.put_parameter(   Name='/alcolizer-rekognition/dev/notifications/config',
                                    Value=pretty,
                                    Type='String',
                                    Overwrite=True 
                                )

if __name__ == "__main__":
    main()
