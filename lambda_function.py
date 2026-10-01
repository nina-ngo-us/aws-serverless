import json
import boto3

# Initialize DynamoDB resource and reference the Users table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    try:
        # Parse the incoming JSON body from API Gateway
        request_body = json.loads(event.get('body', '{}'))
        user_id = request_body.get('userId')
        name = request_body.get('name')
        
        # Validate required fields
        if not user_id or not name:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields: userId and name are required.'})
            }
        
        # Insert item into DynamoDB table
        table.put_item(
            Item={
                'userId': user_id,
                'name': name
            }
        )
        
        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully saved user record.',
                'userId': user_id
            })
        }
        
    except Exception as error:
        # Return internal server error if something goes wrong
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(error)})
        }
