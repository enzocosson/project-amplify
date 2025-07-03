import os
import json
import pytest
from moto import mock_aws
import boto3

from amplify.backend.function.getUser.src.index import handler

table_name = 'userTable'
region = 'eu-west-1'

def create_table_and_user():
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
    # Ajoute un utilisateur
    table.put_item(Item={'userId': '123', 'email': 'test@example.com'})
    return table

@mock_aws
def test_get_user():
    os.environ['USER_TABLE'] = table_name
    os.environ['AWS_REGION'] = region
    create_table_and_user()
    event = {
        'queryStringParameters': {'userId': '123'}
    }
    response = handler(event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['userId'] == '123'
    assert body['email'] == 'test@example.com'

@mock_aws
def test_get_user_not_found():
    os.environ['USER_TABLE'] = table_name
    os.environ['AWS_REGION'] = region
    create_table_and_user()
    event = {
        'queryStringParameters': {'userId': 'notfound'}
    }
    response = handler(event, None)
    assert response['statusCode'] == 404
    assert 'User not found' in response['body']
