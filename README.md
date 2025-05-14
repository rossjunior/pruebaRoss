# API Zonas Deforestadas

## Requisitos

- Python 3.10+
- PostgreSQL + PostGIS
- Acceso a `psql` desde terminal

## Instalación

```bash
# 1. Instala las dependencias
pip install -r requirements.txt

# 2. Ingresa al cliente de PostgreSQL
psql -U postgres

-- 3. Crea la base de datos
CREATE DATABASE deforestacion;
\q

# 4. Conéctate a la nueva base de datos
psql -U postgres -d deforestacion

-- 5. Habilita la extensión PostGIS
CREATE EXTENSION postgis;
\q

# 6. Crea las tablas
python init_db.py

# 7. Inserta datos base (departamentos y tipos de proceso)
python -m app.db.seed

# 8. Inicia la aplicación
uvicorn app.main:app --reload

Swagger UI: http://localhost:8000/docs
```
## Para ejecutarlo mediante docker

- Revisar el archivo DEPLOYMENT.md