# Estimaciones API

API serverless para gestionar estimaciones de lotes catastrales usando AWS Lambda y PostgreSQL RDS.

## Estructura del Proyecto

```
estimaciones-api/
├── serverless.yml          # Configuración de Serverless Framework
├── CrearEstimacion.py      # Lambda para crear estimaciones
├── ListarEstimaciones.py   # Lambda para listar todas las estimaciones
├── BuscarEstimacion.py     # Lambda para buscar estimación por ID
├── ModificarEstimacion.py  # Lambda para modificar estimación existente
├── EliminarEstimacion.py   # Lambda para eliminar estimación
├── db.schema.sql          # Esquema de base de datos
└── README.md              # Este archivo
```

## Endpoints de la API

### 1. Crear Estimación
- **Método**: POST
- **Ruta**: `/estimaciones/crear`
- **Body**: JSON con los datos de la estimación

```json
{
  "num_viviendas": 5,
  "num_comercios": 2,
  "num_industrias": 1,
  "num_educacion": 1,
  "num_salud": 0,
  "num_religion": 1,
  "num_estacionamientos": 10
}
```

### 2. Listar Estimaciones
- **Método**: GET
- **Ruta**: `/estimaciones/listar`
- **Respuesta**: Lista de todas las estimaciones

### 3. Buscar Estimación
- **Método**: POST
- **Ruta**: `/estimaciones/buscar`
- **Body**: JSON con el ID de la estimación

```json
{
  "id": "estimacion_id_here"
}
```

### 4. Modificar Estimación
- **Método**: PUT
- **Ruta**: `/estimaciones/modificar`
- **Body**: JSON con ID y datos a actualizar

```json
{
  "id": "estimacion_id_here",
  "datos": {
    "num_viviendas": 6,
    "num_comercios": 3
  }
}
```

### 5. Eliminar Estimación
- **Método**: DELETE
- **Ruta**: `/estimaciones/eliminar`
- **Body**: JSON con el ID de la estimación

```json
{
  "id": "estimacion_id_here"
}
```

## Campos de la Estimación

- `id`: Identificador único (generado automáticamente)
- `num_viviendas`: Número de viviendas (default: 0)
- `num_comercios`: Número de comercios (default: 0)
- `num_industrias`: Número de industrias (default: 0)
- `num_educacion`: Número de centros de educación (default: 0)
- `num_salud`: Número de centros de salud (default: 0)
- `num_religion`: Número de espacios religiosos (default: 0)
- `num_estacionamientos`: Número de estacionamientos (default: 0)
- `fecha_creacion`: Timestamp de creación (automático)
- `fecha_modificacion`: Timestamp de modificación (automático)

## Despliegue

Para desplegar la API:

```bash
cd estimaciones-api
serverless deploy
```

## Base de Datos

La API utiliza PostgreSQL RDS con la tabla `estimacion`. El esquema SQL está disponible en `db.schema.sql` y se ejecuta automáticamente cuando se crea la instancia RDS.

### Configuración RDS:
- **Motor**: PostgreSQL 15.4
- **Instancia**: db.t3.micro
- **Almacenamiento**: 20 GB (gp2)
- **Cifrado**: Habilitado
- **Backup**: 7 días de retención
- **Acceso**: Público (para desarrollo)

## Configuración

- **Runtime**: Python 3.13
- **Memory**: 1024 MB
- **Timeout**: 20 segundos
- **CORS**: Habilitado para todos los endpoints
- **Dependencias**: psycopg2-binary para conexión PostgreSQL

## Variables de Entorno

Las siguientes variables de entorno se configuran automáticamente:
- `DB_HOST`: Endpoint de la instancia RDS
- `DB_NAME`: Nombre de la base de datos (estimaciones)
- `DB_USER`: Usuario de la base de datos (admin)
- `DB_PASSWORD`: Contraseña de la base de datos (configurable via env var DB_PASSWORD)

## Inicialización de la Base de Datos

La base de datos se inicializa automáticamente cuando se despliega el stack usando un Custom Resource de CloudFormation que ejecuta el esquema SQL definido en `db.schema.sql`.
