import boto3
import os
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Variables
REGION = 'us-east-1'
CRAWLER=os.environ['GLUE_CRAWLER']

# Import Boto 3 for AWS Glue
import boto3
from botocore.exceptions import ClientError
glue = boto3.client(service_name='glue', region_name=REGION)


# Define Lambda function
def lambda_handler(event, context):
    try:
        logger.info('## TRIGGERED BY S3 PUT EVENT')
        logger.info(f'## STARTING GLUE CRAWLER: {CRAWLER}')
        glue.start_crawler(Name=CRAWLER)
    except ClientError as e:
        if e.response.get('Error', {}).get('Code') == 'CrawlerRunningException':
            logger.info(f'## GLUE CRAWLER: {CRAWLER} ALREADY RUNNING')
        else:
            raise e