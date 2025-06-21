import boto3
import json

def lambda_handler(event, context):
    # Parsear el body como JSON
    try:
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Body inválido, debe ser JSON'})
        }

    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')

    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Faltan tenant_id o alumno_id'})
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )

    item = response.get('Item')

    return {
        'statusCode': 200 if item else 404,
        'body': json.dumps(item if item else {'error': 'Alumno no encontrado'})
    }
