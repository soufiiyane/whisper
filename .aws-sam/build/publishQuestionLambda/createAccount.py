import json
import boto3
import uuid
import datetime

def lambda_handler(event, context):
    try:
        if 'body' not in event or event['httpMethod'] != 'POST':
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'Bad Request'})
            }

        body = json.loads(event["body"])

        if 'firstName' not in body or "lastName" not in body or 'userName' not in body or "password" not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'Missing fields in request body'})
            }


        firstName = body["firstName"]
        lastName = body["lastName"]
        userName = body["userName"]
        password = body["password"]
        Id = str(uuid.uuid4())
        Date = str(datetime.datetime.now())

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('users')
        response = table.scan(
            FilterExpression='userName = :userName',
            ExpressionAttributeValues={
                ':userName': userName
            }
        )
        items = response.get('Items', [])
        if items:
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': f"this userName already taken '{userName}':"})
            }
        else:
            user = {
                'Id': Id,
                'Date': Date,
                'firstName': firstName,
                'lastName': lastName,
                'userName': userName,
                'password': password
            }
            table.put_item(Item=user)
            return {
                'statusCode': 200,
                'body': json.dumps({'firstName': firstName, "Id": Id, "Date": Date})
            }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'msg': 'Invalid JSON format'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'msg': 'Internal server error', 'error': str(e)})
        }
