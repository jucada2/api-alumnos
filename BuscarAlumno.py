import boto3

def lambda_handler(event, context):
    tenant_id = event['queryStringParameters']['tenant_id']
    alumno_id = event['queryStringParameters']['alumno_id']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )

    item = response.get('Item', None)

    return {
        'statusCode': 200 if item else 404,
        'alumno': item
    }
