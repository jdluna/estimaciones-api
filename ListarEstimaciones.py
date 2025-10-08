import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Entrada (json)
    # Proceso
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('estimaciones')
        
        # Escanear toda la tabla
        response = table.scan()
        
        estimaciones = response.get('Items', [])
        
        # Salida (json)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'num_reg': len(estimaciones),
                'estimaciones': estimaciones
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error al listar estimaciones: {str(e)}'
            })
        }
