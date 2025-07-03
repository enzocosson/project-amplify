import os
import json
import pytest
from moto import mock_aws
import boto3

# Importer le handler
from amplify.backend.function.postUser.src.index import handler

table_name = 'userTable'

def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')  # eu-west-1 = Irlande
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

@mock_aws
def test_post_user():
    os.environ['USER_TABLE'] = table_name
    os.environ['AWS_REGION'] = 'eu-west-1'  # eu-west-1 = Irlande
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
