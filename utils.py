#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import boto3
import datetime
import json
import os
import requests
from requests_aws4auth import AWS4Auth

GLOBAL_INDEX = 0
URL = 'https://search-photos-tqw5mqdwdbjtscuflf72nc2vg4.us-east-1.es.amazonaws.com/photos/{}'

def send_signed(method, url, service='es', region='us-east-1', body=None):
    credentials = boto3.Session().get_credentials()
    auth = AWS4Auth(credentials.access_key, credentials.secret_key, 
                  region, service, session_token=credentials.token)

    fn = getattr(requests, method)
    if body and not body.endswith("\n"):
        body += "\n"
    try:
        response = fn(url, auth=auth, data=body, 
                        headers={"Content-Type":"application/json"})
        print(response)
        if response.status_code >= 300:
            raise Exception("{} failed with status code {}".format(method.upper(), response.status_code))
        return response.content
    except Exception:
        raise

def es_index(ndjson):
    '''Index new data from `newline delimited JSON` string'''
    # or can put `restaurant` in actions of source json
    # url = URL.format('_bulk?pretty&refresh')
    url = URL.format('_doc')
    send_signed('post', url, body=json.dumps(ndjson))

def es_search(criteria):
    url = URL.format('_search')
    return send_signed('get', url, body=json.dumps(criteria))

def es_store_new_photo(photo):
    """
    Param: photo is a json like:
    {
        "objectKey": "my-photo.jpg",
        "bucket": "my-photo-bucket",
        "labels": ["person", "dog", "ball", "park"]
    }
    """
    photo["createdTimestamp"] = str(datetime.datetime.now())
    es_index(photo)
def es_search_photo_by_label(labels):
    """
    Param: labels is list of keywords: str
    Return a list of photos, each photo is a dict like
    {
        "objectKey": “my-photo.jpg",
        "bucket": "my-photo-bucket",
        "labels": ["person", "dog", "ball", "park"]
    }
    """
    photos = list()
    for label in labels:
        res = es_search({"query": {"match": {"labels": label}}})
        photos.extend([h["_source"] for h in json.loads(res)["hits"]["hits"]])
    return photos
