import json
import boto3

def lambda_handler(event, context):
    # Entrada (json)
    estimacion_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    estimacion_id = estimacion_data['id']
    
    # Proceso
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('estimaciones')
        
        # Buscar estimación por ID
        response = table.get_item(
            Key={
                'estimacion_id': estimacion_id
            }
        )
        
        if 'Item' in response:
            estimacion = response['Item']
            
            # Salida (json)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'estimacion': estimacion
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Estimación no encontrada'
                })
            }
                
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error al buscar estimación: {str(e)}'
            })
        }
