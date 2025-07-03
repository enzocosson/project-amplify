import json
import boto3
import os
from boto3.dynamodb.conditions import Attr

def handler(event, context):
    print('received event:')
    print(event)
    try:
        region = os.environ.get('AWS_REGION', 'eu-west-1')
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table_name = os.environ.get('USER_TABLE', 'userTable')
        table = dynamodb.Table(table_name)
        params = event.get('queryStringParameters') or {}
        email = params.get('email')
        if not email:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps('email is required')
            }
        # Correction de l'import pour Attr
        response = table.scan(
            FilterExpression=Attr('email').eq(email)
        )
        items = response.get('Items', [])
        if not items:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps('User not found')
            }
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(items[0])
        }
    except Exception as e:
        print('Error:', str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('Internal server error: ' + str(e))
        }