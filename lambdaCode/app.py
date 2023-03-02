import boto3
import os
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Variables
REGION = 'us-east-1'
TRIGGER=os.environ['TRIGGER']

# from botocore.exceptions import ClientError
glue = boto3.client(service_name='glue', region_name=REGION)


# Define Lambda function
def lambda_handler(event, context):
    try:
        logger.info('## TRIGGERED BY S3 PUT EVENT')
        logger.info(f'## STARTING GLUE TRIGGER: {TRIGGER}')
        response = glue.start_trigger(Name=TRIGGER)
        return response
    except Exception as e:
        raise e
        # if e.response.get('Error', {}).get('Code') == 'CrawlerRunningException':
        #     logger.info(f'## GLUE TRIGGER: {TRIGGER} ALREADY RUNNING')
        # else:
        #     raise e
    