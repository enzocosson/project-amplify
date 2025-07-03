import json
import boto3
import os

def handler(event, context):
    print('received event:')
    print(event)
    try:
        region = os.environ.get('AWS_REGION', 'eu-west-1')
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table_name = os.environ.get('USER_TABLE', 'userTable')
        table = dynamodb.Table(table_name)
        body = json.loads(event.get('body', '{}'))
        user_id = body.get('userId')
        email = body.get('email')
        if not user_id or not email:
            return {
                'statusCode': 400,
                'body': json.dumps('userId and email are required')
            }
        # Insertion dans DynamoDB
        table.put_item(
            Item={
                'userId': user_id,
                'email': email
            }
        )
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'message': 'User created', 'userId': user_id, 'email': email})
        }
    except Exception as e:
        print('Error:', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error: ' + str(e))
        }