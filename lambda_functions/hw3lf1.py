#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 21:19:35 2020

@author: zyy
"""


import json
import collections
import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)
from util import *
import base64
import random
import string
from datetime import datetime

# def img_info(event):
#     info = event['Records'][-1]
#     bucket = info['s3']['bucket']['name']
#     img = info['s3']['object']['key'].replace('+', ' ')
#     stamp_time =info['eventTime']
#     print('bucket type', type(bucket), type("bucket"))
#     print(img, bucket, stamp_time)
#     return bucket,img,stamp_time


def img_info(event):
	s3 = boto3.client("s3")
	# retrieving data from event
	get_file_content = event["body"]
	file_name = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '.jpg'
	print(file_name)
	
	# decoding data
	file = base64.b64decode(get_file_content)
	bucket = "photob2"
	# uploading file to S3 bucket
	s3_upload = s3.put_object(Bucket="photob2", Key=file_name, Body=file)
	stamp_time = datetime.now()
	
	return bucket, file_name, stamp_time
    
    
def reko_label(img_input):
    reko = boto3.client('rekognition')
    # print("sucessfully")
    response = reko.detect_labels(Image=img_input,MaxLabels=10)
    # print("sucessfully")
    logger.info('get label sucessfully')
    # label = response['Labels']
    label_list = []
    for label in response['Labels']:
        label_list.append(label["Name"])
    print(label_list)
    return label_list
    
    
def convert_json(bucket,img,stamp_time,label_list):
    json = {
        "objectKey": img,
        "bucket": bucket,
        "createdTimestamp": stamp_time,
        "labels": label_list
        
    }
    return json


def lambda_handler(event, context):
    print(event)
    # TODO implement
    bucket,img,stamp_time =  img_info(event)
    img_input = {'S3Object': {'Bucket': bucket, 'Name': img}}
    # print(img_input)
    img_labels = reko_label(img_input)
    img_j = convert_json(bucket, img, stamp_time, img_labels)
    print('img_j', img_j)
    logger.info("json with type :{}, {}".format(type(img_j), img_j))
    es_store_new_photo(img_j)
    logger.info('Successfully uploaded to ES')
    return {
        'statusCode': 200,
        'body': img_j
    }
