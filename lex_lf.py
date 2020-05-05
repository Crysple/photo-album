import json
import boto3
import uuid
from botocore.vendored import requests
from requests_aws4auth import AWS4Auth
from utils import *

def generate_id():
    return uuid.uuid4().hex
    

def lambda_handler(event, context):
    """
    Param: labels is list of keywords: str
    Return a list of photos, each photo is a dict like
    
    """
    # query = event['q']
    print(event)
    query = event["params"]["querystring"]["q"]
    # query = query.encode()
    print("[DEBUG]: ", query)
    client = boto3.client('lex-runtime')
    user_id = generate_id()
    response = client.post_text(
                                botName='SearchQuery',
                                botAlias='search',
                                userId=user_id,
                                inputText=query
                                # contentType="text/plain; charset=utf-8",
                                # inputStream=query 
                            )
    print(response)
    # {'ResponseMetadata': {'RequestId': 'c79517e8-eb90-41ff-a1db-654099033dd4', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'date': 'Thu, 30 Apr 2020 00:49:38 GMT', 'x-amzn-requestid': 'c79517e8-eb90-41ff-a1db-654099033dd4', 'content-length': '291', 'connection': 'keep-alive'}, 'RetryAttempts': 0}, 
    # 'intentName': 'SearchIntent', 'slots': {'objects': 'cats'}, 'message': 'cats', 'messageFormat': 'PlainText', 'dialogState': 'Fulfilled', 'sessionId': '2020-04-30T00:49:38.326Z-MQYjLhNz'}
    
    # {'ResponseMetadata': {'RequestId': '2994cb3c-1d32-4295-bc6a-b5fe7d0bf77e', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'date': 'Thu, 30 Apr 2020 03:58:14 GMT', 'x-amzn-requestid': '2994cb3c-1d32-4295-bc6a-b5fe7d0bf77e', 'content-length': '313', 'connection': 'keep-alive'}, 'RetryAttempts': 0}, 
    # 'intentName': 'SearchIntent', 'slots': {'objects': 'cats', 'objects_two': 'dogs'}, 'dialogState': 'ReadyForFulfillment', 'sessionId': '2020-04-30T03:58:14.298Z-VZRVVped'}
    
    # {'ResponseMetadata': {'RequestId': '71dd18f0-898a-4850-ac8c-6592d984036c', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'date': 'Thu, 30 Apr 2020 04:10:45 GMT', 'x-amzn-requestid': '71dd18f0-898a-4850-ac8c-6592d984036c', 'content-length': '300', 'connection': 'keep-alive'}, 'RetryAttempts': 0}, 'message': 'Sorry, can you please repeat that?', 'messageFormat': 'PlainText', 'dialogState': 'ElicitIntent', 'sessionId': '2020-04-30T04:10:45.920Z-MwFPKzTj'}

    if 'slots' not in response:
        return {'status': False,
                'message': []
                }
    slots = []            
    for key, val in response['slots'].items():
        if slots != None:
            slots.append(val)
    
    print("slots: ", slots)

    photos = es_search_photo_by_label([slot for slot in slots if slot])
    print(photos)
    return {
        'status': True,
        'message': photos
    }
    
    