import json

def lambda_handler(event, context):
    print(event)
    # print(context)
    # q = event['queryStringParameters']['q']
    q = event["params"]["querystring"]["q"]
    print(q)
    return {
        "state": 200,
        'body': q
    }
    