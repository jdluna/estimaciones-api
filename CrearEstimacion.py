import json
import boto3
import uuid
from datetime import datetime

def lambda_handler(event, context):
    # Entrada (json)
    estimacion_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    
    # Validar lote_id requerido
    if 'lote_id' not in estimacion_data:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'lote_id es requerido'
            })
        }
    
    lote_id = estimacion_data['lote_id']
    
    # Validar que lote_id sea un entero de 1 a 8 dígitos
    if not isinstance(lote_id, int) or lote_id < 1 or lote_id > 99999999:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'lote_id debe ser un número entero de 1 a 8 dígitos (entre 1 y 99999999)'
            })
        }
    
    # Proceso
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('estimaciones')
        
        # Generar ID único
        estimacion_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Crear item para DynamoDB
        item = {
            'estimacion_id': estimacion_id,
            'lote_id': lote_id,
            'num_viviendas': estimacion_data.get('num_viviendas', 0),
            'num_comercios': estimacion_data.get('num_comercios', 0),
            'num_industrias': estimacion_data.get('num_industrias', 0),
            'num_educacion': estimacion_data.get('num_educacion', 0),
            'num_salud': estimacion_data.get('num_salud', 0),
            'num_religion': estimacion_data.get('num_religion', 0),
            'num_estacionamientos': estimacion_data.get('num_estacionamientos', 0),
            'fecha_creacion': timestamp,
            'fecha_modificacion': timestamp
        }
        
        # Insertar en DynamoDB
        table.put_item(Item=item)
        
        # Salida (json)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Estimación creada exitosamente',
                'estimacion_id': estimacion_id,
                'lote_id': lote_id,
                'fecha_creacion': timestamp,
                'fecha_modificacion': timestamp
            })
        }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error al crear estimación: {str(e)}'
            })
        }
