# aws-alcolizer-rekognition
The objectives of this project are to encourage every Fortescue team member to self-test at the Alcolizer wall mounted breathalysers and to capture know who has completed a breath test and whether a positive result was returned.

This software project will capture the email, parse the json attachment, store the re-constructed photos and data, and use the AWS Rekognition service to identitfy the person who's photo was taken during the Alcolizer breathalyser test.

The AWS Simple Email Service will be used to capture the email that was sent directly from the Alcolizer, and to "Put" the email attachment into an S3 Bcuket.
The StepFuntion will orchestrate the processing of the contents and create a single json output of the result and put that into a dedciated S3 Bucket.
The Snowflake Snowpipe service will capture each file and be resonsible for ingesting the contents in near-realtime into Snbowflake. 

The AWS rekognition Collection will be updated with new Hires by a separate AWS batch job which will extract the photos from the Gallagher Card System nightly.


