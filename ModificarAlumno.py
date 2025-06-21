import boto3
import json

def lambda_handler(event, context):
    # Obtener y parsear el body según su tipo (dict o string JSON)
    raw_body = event.get('body', {})
    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'El body debe ser un JSON válido'})
            }
    else:
        body = raw_body

    # Extraer campos requeridos
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')
    alumno_datos = body.get('alumno_datos')

    if not tenant_id or not alumno_id or not alumno_datos:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Faltan tenant_id, alumno_id o alumno_datos'})
        }

    # Conexión a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    # Actualizar el item
    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        UpdateExpression="SET alumno_datos = :datos",
        ExpressionAttributeValues={
            ':datos': alumno_datos
        },
        ReturnValues="ALL_NEW"
    )

    updated_item = response.get('Attributes', {})

    return {
        'statusCode': 200,
        'body': json.dumps(updated_item)
    }
