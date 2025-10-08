import json
import psycopg2
import os
from datetime import datetime

def lambda_handler(event, context):
    # Entrada (json)
    estimacion_data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    estimacion_id = estimacion_data['id']
    datos = estimacion_data['datos']
    
    # Proceso
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
        
        with conn.cursor() as cursor:
            # Construir query de actualización dinámicamente
            update_fields = []
            values = []
            
            # Agregar campos a actualizar
            if 'num_viviendas' in datos:
                update_fields.append("num_viviendas = %s")
                values.append(datos['num_viviendas'])
            
            if 'num_comercios' in datos:
                update_fields.append("num_comercios = %s")
                values.append(datos['num_comercios'])
            
            if 'num_industrias' in datos:
                update_fields.append("num_industrias = %s")
                values.append(datos['num_industrias'])
            
            if 'num_educacion' in datos:
                update_fields.append("num_educacion = %s")
                values.append(datos['num_educacion'])
            
            if 'num_salud' in datos:
                update_fields.append("num_salud = %s")
                values.append(datos['num_salud'])
            
            if 'num_religion' in datos:
                update_fields.append("num_religion = %s")
                values.append(datos['num_religion'])
            
            if 'num_estacionamientos' in datos:
                update_fields.append("num_estacionamientos = %s")
                values.append(datos['num_estacionamientos'])
            
            # Agregar fecha de modificación
            update_fields.append("fecha_modificacion = %s")
            values.append(datetime.now())
            
            # Agregar ID al final de los valores
            values.append(estimacion_id)
            
            # Ejecutar actualización
            update_query = f"""
                UPDATE estimacion 
                SET {', '.join(update_fields)}
                WHERE id = %s
                RETURNING id, fecha_modificacion
            """
            
            cursor.execute(update_query, values)
            result = cursor.fetchone()
            conn.commit()
            
            if result:
                # Salida (json)
                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'Estimación modificada exitosamente',
                        'id': result[0],
                        'fecha_modificacion': result[1].isoformat()
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
    finally:
        if 'conn' in locals():
            conn.close()
