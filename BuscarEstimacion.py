import json
import psycopg2
import os

def lambda_handler(event, context):
    # Entrada (json)
    estimacion_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    estimacion_id = estimacion_data['id']
    
    # Proceso
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        
        with conn.cursor() as cursor:
            # Buscar estimación por ID
            cursor.execute("""
                SELECT id, num_viviendas, num_comercios, num_industrias, 
                       num_educacion, num_salud, num_religion, num_estacionamientos,
                       fecha_creacion, fecha_modificacion
                FROM estimacion
                WHERE id = %s
            """, (estimacion_id,))
            
            row = cursor.fetchone()
            
            if row:
                estimacion = {
                    'id': row[0],
                    'num_viviendas': row[1],
                    'num_comercios': row[2],
                    'num_industrias': row[3],
                    'num_educacion': row[4],
                    'num_salud': row[5],
                    'num_religion': row[6],
                    'num_estacionamientos': row[7],
                    'fecha_creacion': row[8].isoformat() if row[8] else None,
                    'fecha_modificacion': row[9].isoformat() if row[9] else None
                }
                
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
    finally:
        if 'conn' in locals():
            conn.close()
