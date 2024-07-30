import boto3
import json
import os
import datetime


def lambda_handler(event, context):
    cognito_client = boto3.client('cognito-idp')
    dynamodb_client = boto3.resource('dynamodb')

    user_pool_id = os.environ['USER_POOL_ID']
    table_name = "questions"

    try:
        if 'body' not in event:
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
        question = body["question"]

        response = cognito_client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=uuid
        )

        username = response['Username']
        attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
        family_name = attributes.get('family_name', 'Unknown')
        given_name = attributes.get('given_name', 'Unknown')

        question_item = {
            'userName': username,
            'question': question,
            'Date': str(datetime.datetime.now())
        }
        table_questions = dynamodb_client.Table(table_name)

        table_questions.put_item(Item=question_item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'msg': f'Your question has been published successfully to user {family_name} {given_name}'
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except cognito_client.exceptions.UserNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
