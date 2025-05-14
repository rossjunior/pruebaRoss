# PRUEBA ROSS JR TIQUE MONTOYA

# Guía de Despliegue del Sistema de Zonas Deforestadas

## Arquitectura del Sistema

El sistema de Zonas Deforestadas es una API RESTful construida con FastAPI que permite gestionar información geoespacial sobre zonas deforestadas. La arquitectura del sistema incluye:

- **Backend**: API RESTful desarrollada con FastAPI
- **Base de datos**: PostgreSQL con extensión PostGIS para datos geoespaciales
- **Contenedores**: Docker para facilitar el despliegue y la portabilidad
- **Herramientas adicionales**: pgAdmin para administración de la base de datos

## Requisitos Previos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Git (para clonar el repositorio)

## Despliegue con Docker

### 1. Clonar el Repositorio

```bash
git clone https://github.com/rossjunior/pruebaRoss.git
cd pruebaRoss
```

### 2. Configuración de Variables de Entorno

El sistema utiliza archivos `.env` para la configuración. Para despliegue con Docker, se utiliza el archivo `.env.docker`:

```bash
# El archivo .env.docker ya está configurado con:
DATABASE_URL=postgresql://postgres:postgres@db:5432/deforestacion
```

Si necesitas personalizar la configuración, puedes modificar este archivo o crear uno nuevo y actualizar la referencia en `docker-compose.yml`.

### 3. Iniciar los Servicios con Docker Compose

```bash
docker-compose up -d
```

Este comando iniciará tres servicios:

- **web**: La API FastAPI (accesible en http://localhost:8000)
- **db**: Base de datos PostgreSQL con PostGIS (accesible en localhost:5432)
- **pgadmin**: Interfaz web para administrar la base de datos (accesible en http://localhost:5050)

### 4. Verificar el Despliegue

Para verificar que la API está funcionando correctamente:

```bash
curl http://localhost:8000/docs
```

Esto debería mostrar la documentación interactiva de la API (Swagger UI).

## Estructura de la Base de Datos

La base de datos `deforestacion` contiene las siguientes tablas principales:

- **departamentos**: Información sobre departamentos geográficos
- **tipos_procesos**: Tipos de procesos de deforestación
- **zonas_deforestadas**: Información geoespacial sobre zonas deforestadas

La extensión PostGIS permite almacenar y consultar datos geoespaciales como polígonos que representan las zonas deforestadas.

### Acceso a pgAdmin

1. Accede a http://localhost:5050
2. Inicia sesión con:
   - Email: admin@admin.com
   - Password: admin
3. Configura una nueva conexión al servidor:
   - Host: db
   - Port: 5432
   - Database: deforestacion
   - Username: postgres
   - Password: admin

## Endpoints de la API

La API proporciona los siguientes endpoints principales:

- **Zonas Deforestadas**:
  - `GET /zonas-deforestadas/`: Listar todas las zonas
  - `GET /zonas-deforestadas/{id}`: Obtener una zona específica
  - `POST /zonas-deforestadas/`: Crear una nueva zona
  - `PUT /zonas-deforestadas/{id}`: Actualizar una zona existente
  - `DELETE /zonas-deforestadas/{id}`: Eliminar una zona

- **Departamentos**:
  - `GET /api/departamentos/`: Listar todos los departamentos
  - `GET /api/departamentos/{id}`: Obtener un departamento específico
  - `POST /api/departamentos/`: Crear un nuevo departamento
  - `PUT /api/departamentos/{id}`: Actualizar un departamento existente
  - `DELETE /api/departamentos/{id}`: Eliminar un departamento

- **Tipos de Procesos**:
  - `GET /api/tipos_proceso/`: Listar todos los tipos de procesos
  - `GET /api/tipos_proceso/{id}`: Obtener un tipo de proceso específico
  - `POST /api/tipos_proceso/`: Crear un nuevo tipo de proceso
  - `PUT /api/tipos_proceso/{id}`: Actualizar un tipo de proceso existente
  - `DELETE /api/tipos_proceso/{id}`: Eliminar un tipo de proceso

Para una documentación completa de la API, accede a http://localhost:8000/docs cuando el servicio esté en ejecución.

## Desarrollo Local

Para desarrollo local sin Docker, puedes seguir estos pasos:

1. Instalar PostgreSQL con PostGIS localmente
2. Crear una base de datos `deforestacion`
3. Configurar el archivo `.env` con la URL de conexión a tu base de datos local
4. Instalar las dependencias: `pip install -r requirements.txt`
5. Iniciar el servidor: `uvicorn app.main:app --reload`

## Pruebas

El sistema incluye pruebas unitarias que puedes ejecutar con:

```bash
pytest
```

Para ejecutar pruebas específicas:

```bash
pytest tests/test_zonas.py
pytest tests/test_departamentos.py
pytest tests/test_tipos_procesos.py
```

## Escalamiento y Producción

Para un entorno de producción, considera:

1. **Seguridad**:
   - Cambiar las contraseñas predeterminadas
   - Configurar HTTPS con certificados SSL
   - Implementar un proxy inverso como Nginx

2. **Respaldo**:
   - Configurar respaldos automáticos de la base de datos
   - Utilizar volúmenes Docker persistentes

3. **Monitoreo**:
   - Implementar herramientas de monitoreo como Prometheus y Grafana
   - Configurar alertas para problemas de rendimiento o disponibilidad

## Solución de Problemas Comunes

### La API no responde

1. Verifica que los contenedores estén en ejecución:
   ```bash
   docker-compose ps
   ```

2. Revisa los logs de la aplicación:
   ```bash
   docker-compose logs web
   ```

### Problemas con la Base de Datos

1. Verifica que el contenedor de la base de datos esté en ejecución:
   ```bash
   docker-compose ps db
   ```

2. Revisa los logs de la base de datos:
   ```bash
   docker-compose logs db
   ```

3. Intenta reiniciar el contenedor:
   ```bash
   docker-compose restart db
   ```

### Reinicio Completo

Si necesitas reiniciar completamente el sistema:

```bash
docker-compose down
docker-compose up -d
```

Para reiniciar y eliminar todos los datos (¡precaución!):

```bash
docker-compose down -v
docker-compose up -d
```

## Comandos Docker Útiles

- **Ver contenedores en ejecución**: `docker ps`
- **Ver logs de un contenedor**: `docker logs [container_id]`
- **Ejecutar comandos en un contenedor**: `docker exec -it [container_id] [command]`
- **Acceder a la base de datos**: `docker exec -it pruebaross_db_1 psql -U postgres -d deforestacion`
- **Detener todos los servicios**: `docker-compose down`

## Recursos Adicionales

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de PostgreSQL](https://www.postgresql.org/docs/)
- [Documentación de PostGIS](https://postgis.net/documentation/)
- [Documentación de Docker](https://docs.docker.com/)
