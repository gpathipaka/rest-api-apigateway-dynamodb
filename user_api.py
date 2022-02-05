import json
import boto3
import uuid
import time

dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):
    
    print(f'Event {event}')
    # TODO implement
    if event['httpMethod'] == 'GET':
        try:
            return doget(event)
        except Exception as e:
            return get_response(500, 'Get failed ' + str(e))
    elif event['httpMethod'] == 'POST':
        try:
            return docreate(event)
        except Exception as e:
            return get_response(500, 'Create failed ' + str(e))
    elif event['httpMethod'] == 'PUT':
        try:
            return update(event) 
        except Exception as e:
            return get_response(500, 'Update failed ' + str(e))
       
    elif event['httpMethod'] == 'DELETE':
        try:
            return dodelete(event)
        except Exception as e:
            return get_response(500, 'delete failed ' + str(e))
    else:
        return get_response(405, 'Not supported')

def doget(event):
    print('starting doget()')
    params = 'queryStringParameters'
    table = dynamodb.Table('user')
    if event[params] is not None:
        userId = event[params]['userId']
        print('searching for ' + userId)
        response = table.get_item(
            Key={'userId': userId})
        return get_response(200, response['Item'])
    else:
        print('Getting all the users')
        response = table.scan()
        print(f'******** Response {response}')
        return get_response(200, response['Items'])
    return get_response(204, 'User Not found')
    
def docreate(event):
    print('starting docreate()')
    body = event['body']
    userId = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time()))).split('-')[4]
    try:
        # TODO: write code...
        body = json.loads(body)
        body['userId'] = userId
        table = dynamodb.Table('user')
        response = table.put_item(
           Item=body
        )
        print(f'Dynamodb response : {response}')
    except Exception as e:
        return get_response(500, 'User Create failed ' + str(e))
    return get_response(201, 'User Created & userID: ' + userId )
    
def update(event):
    print('starting update()')
    table = dynamodb.Table('user')
    body = event['body']
    print(f'body = {body}')
    body = json.loads(body)
    userId = body['userId']
    fn =  body['firstName']
    ln =  body['lastName']
    print(f'{userId} - {fn} - {ln} ')
    response = table.update_item(
        Key={'userId': userId},
        UpdateExpression="set firstName = :f, lastName = :l",
        ExpressionAttributeValues={
                ':f':fn,
                ':l':ln
            }
        )
    print(f'******* {response}')
    return get_response(200, 'User Updated')
    
def dodelete(event):
    print('starting delete()')
    table = dynamodb.Table('user')
    body = event['body']
    print(f'body = {body}')
    body = json.loads(body)
    userId = body['userId']
    response = table.update_item(
        Key = {'userId': userId}
        )
    print(f'Delete Response {response}')
    return get_response(200, 'User Deleted')
def get_response(code, message):
    return {
            'statusCode': code,
            'body': json.dumps(message)
        }