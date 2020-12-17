# sa-launch
December 2020 Team 4 SA-Launch

## Background

This repository contains code for the Team 4 SA Launch Covid Test Locator project.  

The covidTestLocator.py file contains a lambda function for a Lex bot which will resolve the closest Covid test center given a 
person's Zipcode.

See the SAM template and package config files as well for deploying to AWS.


## Usage

To Package:

    sam package --s3-bucket=covid-test-locator --region=us-east-1  --output-template-file package.yml


To Deploy:

    sam deploy --template-file /Users/jeffdoto/Desktop/geocoding_test/package.yml --stack-name covid-lambda-stack --region=us-east-1 --capabilities CAPABILITY_IAM