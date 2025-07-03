import os
import json
import pytest
from moto import mock_aws
import boto3

from amplify.backend.function.postUser.src.index import handler

table_name = 'userTable'
region = 'eu-west-1'

def create_table():
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'userId', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'userId', 'AttributeType': 'S'},
            {'AttributeName': 'email', 'AttributeType': 'S'},
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'email-index',
                'KeySchema': [
                    {'AttributeName': 'email', 'KeyType': 'HASH'},
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
            }
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )
    table.wait_until_exists()
    return table

def test_post_user():
    with mock_aws():
        os.environ['USER_TABLE'] = table_name
        os.environ['AWS_REGION'] = region
        create_table()
        event = {
            'body': json.dumps({'userId': '123', 'email': 'test@example.com'})
        }
        response = handler(event, None)
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['userId'] == '123'
        assert body['email'] == 'test@example.com'
        assert body['message'] == 'User created'
