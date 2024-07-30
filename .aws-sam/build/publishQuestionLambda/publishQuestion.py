import boto3
import json
import os


def lambda_handler(event, context):

    try:
        client = boto3.client('cognito-idp')
        user_pool_id = os.environ['USER_POOL_ID']

        if 'body' not in event or event['httpMethod'] != 'POST':
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'Bad Request'})
            }

        body = json.loads(event["body"])
        if 'uuid' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'UUID field is missing'})
            }
        uuid = body["uuid"]
        response = client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=uuid
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'Username': response['Username'],
                'Attributes': {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except client.exceptions.UserNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        # Handle other exceptions
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
