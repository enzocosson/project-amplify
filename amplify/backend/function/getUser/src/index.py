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
        params = event.get('queryStringParameters') or {}
        user_id = params.get('userId')
        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps('userId is required')
            }
        response = table.get_item(Key={'userId': user_id})
        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('User not found')
            }
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(item)
        }
    except Exception as e:
        print('Error:', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error: ' + str(e))
        }