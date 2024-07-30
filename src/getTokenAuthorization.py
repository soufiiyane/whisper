import boto3
import os
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        client = boto3.client('cognito-idp')
        if 'body' not in event or event['httpMethod'] != 'POST':
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'Bad Request'})
            }
        body = json.loads(event["body"])
        if 'email' not in body or "password" not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'Missing fields in request body'})
            }
        username = body["email"]
        password = body["password"]
        response = client.initiate_auth(
            ClientId=os.environ['CLIENT_ID'],
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        id_token = response['AuthenticationResult']['IdToken']

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully signed in',
                'id_token': id_token,
            })
        }

    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': str(e)
            })
        }
