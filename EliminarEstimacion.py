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
            # Eliminar estimación
            cursor.execute("""
                DELETE FROM estimacion 
                WHERE id = %s
                RETURNING id
            """, (estimacion_id,))
            
            result = cursor.fetchone()
            conn.commit()
            
            if result:
                # Salida (json)
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Estimación eliminada exitosamente',
                        'id': result[0]
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
    finally:
        if 'conn' in locals():
            conn.close()
