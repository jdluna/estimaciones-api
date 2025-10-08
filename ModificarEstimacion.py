import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Entrada (json)
    estimacion_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    estimacion_id = estimacion_data['id']
    datos = estimacion_data['datos']
    
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
        
        # Construir expresión de actualización dinámicamente
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        # Agregar lote_id a actualizar
        update_expression += "#lote_id = :lote_id, "
        expression_attribute_names['#lote_id'] = 'lote_id'
        expression_attribute_values[':lote_id'] = lote_id
        
        # Agregar campos a actualizar
        if 'num_viviendas' in datos:
            update_expression += "#viviendas = :viviendas, "
            expression_attribute_names['#viviendas'] = 'num_viviendas'
            expression_attribute_values[':viviendas'] = datos['num_viviendas']
        
        if 'num_comercios' in datos:
            update_expression += "#comercios = :comercios, "
            expression_attribute_names['#comercios'] = 'num_comercios'
            expression_attribute_values[':comercios'] = datos['num_comercios']
        
        if 'num_industrias' in datos:
            update_expression += "#industrias = :industrias, "
            expression_attribute_names['#industrias'] = 'num_industrias'
            expression_attribute_values[':industrias'] = datos['num_industrias']
        
        if 'num_educacion' in datos:
            update_expression += "#educacion = :educacion, "
            expression_attribute_names['#educacion'] = 'num_educacion'
            expression_attribute_values[':educacion'] = datos['num_educacion']
        
        if 'num_salud' in datos:
            update_expression += "#salud = :salud, "
            expression_attribute_names['#salud'] = 'num_salud'
            expression_attribute_values[':salud'] = datos['num_salud']
        
        if 'num_religion' in datos:
            update_expression += "#religion = :religion, "
            expression_attribute_names['#religion'] = 'num_religion'
            expression_attribute_values[':religion'] = datos['num_religion']
        
        if 'num_estacionamientos' in datos:
            update_expression += "#estacionamientos = :estacionamientos, "
            expression_attribute_names['#estacionamientos'] = 'num_estacionamientos'
            expression_attribute_values[':estacionamientos'] = datos['num_estacionamientos']
        
        # Agregar fecha de modificación
        update_expression += "#fecha_modificacion = :fecha_modificacion"
        expression_attribute_names['#fecha_modificacion'] = 'fecha_modificacion'
        expression_attribute_values[':fecha_modificacion'] = datetime.utcnow().isoformat()
        
        # Ejecutar actualización
        response = table.update_item(
            Key={
                'estimacion_id': estimacion_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        
        if 'Attributes' in response:
            # Salida (json)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Estimación modificada exitosamente',
                    'estimacion_id': estimacion_id,
                    'lote_id': lote_id,
                    'fecha_modificacion': response['Attributes'].get('fecha_modificacion')
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
                'error': f'Error al modificar estimación: {str(e)}'
            })
        }
