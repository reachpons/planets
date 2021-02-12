import boto3
from botocore.exceptions import ClientError


SENDER = "ibunney@fmgl.com.au"
RECIPIENT = "shelewis@fmgl.com.au"
AWS_REGION = "ap-southeast-2"
SUBJECT = "Amazon SES Test (SDK for Python)"
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Problem Solved</h1>
  <h2>Amazon SES API & BOTO3 </h2>
  <p>This email was sent by Ian Bunney without SMTP  and is Encrypted and Authenticated   
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.</p>
</body>
</html>
"""            


def main():
    peeps = ["ibunney@fmgl.com.au","shelewis@fmgl.com.au" ]

    itm= { 
        'recipients' : peeps
    }

    print(itm)

def main2():

    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)

    try:   
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    }
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )

    except ClientError as e:
        print(e)
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


if __name__ == "__main__":    
    main()
