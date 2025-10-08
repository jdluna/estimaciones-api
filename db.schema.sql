-- Database schema for estimaciones API
-- This file contains the SQL schema for the estimaciones table

CREATE TABLE IF NOT EXISTS estimacion (
    id SERIAL PRIMARY KEY,
    num_viviendas INTEGER DEFAULT 0,
    num_comercios INTEGER DEFAULT 0,
    num_industrias INTEGER DEFAULT 0,
    num_educacion INTEGER DEFAULT 0,
    num_salud INTEGER DEFAULT 0,
    num_religion INTEGER DEFAULT 0,
    num_estacionamientos INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_estimacion_fecha_creacion ON estimacion(fecha_creacion);
CREATE INDEX IF NOT EXISTS idx_estimacion_fecha_modificacion ON estimacion(fecha_modificacion);

-- Add comments to the table and columns
COMMENT ON TABLE estimacion IS 'Tabla para almacenar estimaciones de lotes catastrales con conteos de diferentes tipos de propiedades';
COMMENT ON COLUMN estimacion.id IS 'Identificador único de la estimación';
COMMENT ON COLUMN estimacion.num_viviendas IS 'Número de viviendas en el lote catastral';
COMMENT ON COLUMN estimacion.num_comercios IS 'Número de comercios en el lote catastral';
COMMENT ON COLUMN estimacion.num_industrias IS 'Número de industrias en el lote catastral';
COMMENT ON COLUMN estimacion.num_educacion IS 'Número de centros de educación en el lote catastral';
COMMENT ON COLUMN estimacion.num_salud IS 'Número de centros de salud en el lote catastral';
COMMENT ON COLUMN estimacion.num_religion IS 'Número de espacios religiosos en el lote catastral';
COMMENT ON COLUMN estimacion.num_estacionamientos IS 'Número de estacionamientos en el lote catastral';
COMMENT ON COLUMN estimacion.fecha_creacion IS 'Fecha y hora de creación del registro';
COMMENT ON COLUMN estimacion.fecha_modificacion IS 'Fecha y hora de la última modificación del registro';
