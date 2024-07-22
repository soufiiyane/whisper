import json
import datetime
import boto3

def lambda_handler(event, context):
    try:
        if 'body' not in event or event['httpMethod'] != 'POST':
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'Bad Request'})
            }
        body = json.loads(event["body"])
        if 'question' not in body or "userName" not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'Missing fields in request body'})
            }
        question = body["question"]
        userName = body["userName"]

        dynamodb = boto3.resource('dynamodb')
        table_users = dynamodb.Table("users")
        response = table_users.scan(
            FilterExpression='userName = :userName',
            ExpressionAttributeValues={
                ':userName': userName
            }
        )
        items = response.get('Items', [])
        if items:
            table_questions = dynamodb.Table("questions")
            question_item = {
                'userName': userName,
                'question': question,
                'Date':  str(datetime.datetime.now())
            }
            table_questions.put_item(Item=question_item)
            return {
                'statusCode': 200,
                'body': json.dumps({'msg': "Question successfully published"})
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'msg': 'no user with this userName'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'msg': 'Internal server error', 'error': str(e)})
        }