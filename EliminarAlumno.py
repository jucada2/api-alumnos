import boto3
import json

def lambda_handler(event, context):
    # Parsear el body (puede ser string o dict)
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

    # Extraer parámetros
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')

    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Faltan tenant_id o alumno_id'})
        }

    # Conexión a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    # Eliminar alumno y verificar si existía
    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        ReturnValues='ALL_OLD'  # Retorna los datos eliminados si existían
    )

    deleted_item = response.get('Attributes')

    if not deleted_item:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Alumno no encontrado'})
        }

    return {
        'statusCode': 200,
        'body': {
            'message': 'Alumno eliminado correctamente',
            'alumno': deleted_item
        }
    }
