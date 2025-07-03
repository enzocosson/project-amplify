import json
import boto3
import os
import uuid

def handler(event, context):
    print('received event:')
    print(event)
    try:
        region = os.environ.get('AWS_REGION', 'eu-west-1')
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table_name = os.environ.get('USER_TABLE', 'userTable')
        table = dynamodb.Table(table_name)
        # Gestion du body qui peut déjà être un dict (cas tests locaux ou invocation directe)
        body_raw = event.get('body', '{}')
        if isinstance(body_raw, dict):
            body = body_raw
        else:
            body = json.loads(body_raw)
        email = body.get('email')
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
        # Générer un userId automatiquement (UUID)
        user_id = str(uuid.uuid4())
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
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('Internal server error: ' + str(e))
        }