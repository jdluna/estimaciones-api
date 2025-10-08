import json
import psycopg2
import os
from datetime import datetime

def lambda_handler(event, context):
    # Entrada (json)
    estimacion_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    
    # Proceso
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        
        with conn.cursor() as cursor:
            # Insertar nueva estimación
            cursor.execute("""
                INSERT INTO estimacion (
                    num_viviendas, num_comercios, num_industrias, 
                    num_educacion, num_salud, num_religion, num_estacionamientos
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, fecha_creacion, fecha_modificacion
            """, (
                estimacion_data.get('num_viviendas', 0),
                estimacion_data.get('num_comercios', 0),
                estimacion_data.get('num_industrias', 0),
                estimacion_data.get('num_educacion', 0),
                estimacion_data.get('num_salud', 0),
                estimacion_data.get('num_religion', 0),
                estimacion_data.get('num_estacionamientos', 0)
            ))
            
            result = cursor.fetchone()
            conn.commit()
            
            # Salida (json)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Estimación creada exitosamente',
                    'id': result[0],
                    'fecha_creacion': result[1].isoformat(),
                    'fecha_modificacion': result[2].isoformat()
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error al crear estimación: {str(e)}'
            })
        }
    finally:
        if 'conn' in locals():
            conn.close()
