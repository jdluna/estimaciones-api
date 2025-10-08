import json
import boto3

def lambda_handler(event, context):
    # Entrada (path parameter)
    estimacion_id = event['pathParameters']['id']
    
    # Proceso
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('estimaciones')
        
        # Eliminar estimación
        response = table.delete_item(
            Key={
                'estimacion_id': estimacion_id
            },
            ReturnValues="ALL_OLD"
        )
        
        if 'Attributes' in response:
            lote_id = response['Attributes'].get('lote_id')
            # Salida (json)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Estimación eliminada exitosamente',
                    'estimacion_id': estimacion_id,
                    'lote_id': lote_id
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
                'error': f'Error al eliminar estimación: {str(e)}'
            })
        }
