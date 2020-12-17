# sa-launch
December 2020 Team 4 SA-Launch

## Background

This repository contains code for the Team 4 SA Launch Covid Test Locator project.  

The covidTestLocator.py file contains a lambda function for a Lex bot which will resolve the closest Covid test center given a 
person's Zipcode.

See the SAM template and package config files as well for deploying to AWS.


## Usage

To install dependencies:
    
    # Note, in this example i've installed python via HomeBrew like this:
    #  brew install python@3.7

    # Create a virtualenv using python 3.7, which our build requires:
    virtualenv --python=/usr/local/Cellar/python@3.7/3.7.9_2/bin/python3 venv

    pip install -r requirements.txt


Installing SAM:

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

Download docker, and log in:

    docker login


To Build:

     sam build --use-container


To Package:

    sam package --s3-bucket=covid-test-locator --region=us-east-1  --output-template-file package.yml  --profile=sa-launch


To Deploy:

    sam deploy --template-file /Users/jeffdoto/Desktop/geocoding_test/package.yml --stack-name covid-lambda-stack --region=us-east-1 --capabilities CAPABILITY_IAM

