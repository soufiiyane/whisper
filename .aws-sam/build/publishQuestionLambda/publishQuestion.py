import json
import datetime
import boto3

def lambda_handler(event, context):
    try:
        return {
            'statusCode': 200,
            'body': json.dumps({'msg': "Question successfully published"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'msg': 'Internal server error', 'error': str(e)})
        }