# aws-alcolizer-rekognition
The objectives of this project are to encourage every Fortescue team member to self-test at the Alcolizer wall mounted breathalysers and to capture know who has completed a breath test and whether a positive result was returned.

This software project will capture the email, parse the json attachment, store the re-constructed photos and data, and use the AWS Rekognition service to identitfy the person who's photo was taken during the Alcolizer breathalyser test.

The AWS Simple Email Service will be used to capture the email that was sent directly from the Alcolizer, and to "Put" the email attachment into an S3 Bcuket.
The StepFuntion will orchestrate the processing of the contents and create a single json output of the result and put that into a dedciated S3 Bucket.
The Snowflake Snowpipe service will capture each file and be resonsible for ingesting the contents in near-realtime into Snbowflake. 

The AWS rekognition Collection will be updated with new Hires by a separate AWS batch job which will extract the photos from the Gallagher Card System nightly.

How to populate the Alcolizer Collection index

Step-1 Clone this repo and execute below command from newhire folder

	aws cloudformation create-stack --stack-name NewHireBatch --template-body file://CreateAWSInfrastructure.yaml --parameters file://Parameter.json  --capabilities CAPABILITY_NAMED_IAM

This cloudformation stack will create below AWS resources 
1. AWS roles required form AWS batch
2. AWS role for Cloud watch event.
3. AWS Batch compute environment of type FARGATE
4. AWS Batch Job Queue
5. AWS Job Definition
6. AWS cloudwatch event to trigger the Batch.

Ste-2: Execute below command to create a container and publish into AWS ECR

	.\ECRDockerizer.ps1 alcolizerrepouat

This powershell script dockerise the python app and push the image into AWS ECR.
