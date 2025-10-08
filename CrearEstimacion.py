import json
import boto3
import uuid
from datetime import datetime

def lambda_handler(event, context):
    # Entrada (json)
    estimacion_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    
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
