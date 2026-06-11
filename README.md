# Museo Atrium - Microservicio de Auditoría (Cassandra + Web UI)

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y ejecutándose
- Python 3.10 o superior
- Entorno virtual (venv)

## Estructura del proyecto

```
audit-python-cassandra/
├── app/                     # Lógica de la aplicación (Repositories, Schemas, Routes)
├── docker/
│   └── docker-compose.yml   # Orquestación de contenedores
├── scripts/
│   ├── 0*.cql               # Estructura de tablas (Keyspace y Módulos)
│   └── seed_*.cql           # Datos de prueba iniciales
├── tests/                   # Pruebas de integración automatizadas
├── main.py                  # API FastAPI
├── requirements.txt         # Dependencias de Python
└── README.md
```

## Paso 1: Iniciar los contenedores

Desde la raíz del proyecto, ejecuta:

```powershell
docker compose -f docker/docker-compose.yml up -d
```

Esto levantará tres contenedores:

| Contenedor | Imagen | Puerto | Función |
|---|---|---|---|
| `museo-cassandra-nodo` | `cassandra:4.0` | `9042` | Base de datos Cassandra |
| `museo-cassandra-init` | `cassandra:4.0` | - | Inicializa esquemas y datos semilla automáticamente |
| `museo-cassandra-web` | `delermando/docker-cassandra-web:v0.4.0` | `3000` | Interfaz web de administración |

La primera vez descargará las imágenes, puede tomar varios minutos.

## Paso 2: Verificar que todo esté funcionando

```powershell
docker ps -a
```

Debes ver algo similar a:

```
CONTAINER ID   IMAGE                                    STATUS                        PORTS
xxx            cassandra:4.0                            Up (healthy)                  0.0.0.0:9042->9042/tcp
xxx            cassandra:4.0                            Exited (0)                    (init completado)
xxx            delermando/docker-cassandra-web:v0.4.0   Up                           0.0.0.0:3000->3000/tcp
```

- `museo-cassandra-nodo` debe aparecer como `(healthy)`
- `museo-cassandra-init` debe aparecer como `Exited (0)` (indica que el keyspace y las tablas se crearon correctamente)

## Paso 3: Acceder a CassandraDB Web

Abre tu navegador en:

```
http://localhost:3000
```

La web UI ya está preconfigurada con las siguientes credenciales:

| Campo | Valor |
|---|---|
| **Host** | `172.20.0.10` |
| **Port** | `9042` |
| **Username** | `cassandra` |
| **Password** | `cassandra` |

La conexión se establece automáticamente al cargar la página. Verás el keyspace `museo_auditoria` listo para explorar.

## Paso 4: Usar la interfaz web

Una vez conectado puedes:

- **Explorar keyspaces y tablas** en el panel lateral izquierdo
- **Ejecutar consultas CQL** en la pestaña "Query"
- **Ver datos** haciendo clic en cualquier tabla
- **Administrar el esquema** (crear tablas, índices, etc.)

## Paso 5: Ejecutar el API Python

1. **Crear y activar el entorno virtual:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Instalar dependencias:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Iniciar el servidor:**
   ```powershell
   uvicorn main:app --reload
   ```

Accede a la documentación interactiva en: `http://127.0.0.1:8000/docs`.

## Paso 6: Ejecutar Pruebas Automatizadas

El proyecto incluye una suite de pruebas de integración para validar el funcionamiento de los endpoints:

```powershell
python -m pytest tests/test_api.py -v
```

## Comandos útiles

```powershell
# Iniciar todos los contenedores
docker compose -f docker/docker-compose.yml up -d

# Ver logs del proceso de inicialización de la base de datos
docker logs museo-cassandra-init

# Detener los contenedores (sin borrar datos)
docker compose -f docker/docker-compose.yml down

# Detener y borrar todos los datos (volumen)
docker compose -f docker/docker-compose.yml down -v

# Conectarse a Cassandra vía cqlsh (terminal interactiva)
docker exec -it museo-cassandra-nodo cqlsh
```

## Solución de problemas

### El contenedor Cassandra no se pone healthy
```powershell
docker logs museo-cassandra-nodo
```
Espera unos segundos, Cassandra puede tardar hasta 60s en inicializarse.

### Error "unsupported release version"
Si ves este error en la web UI, significa que la imagen `cassandra-web` es incompatible con la versión de Cassandra. Asegúrate de usar `cassandra:4.0` (no `latest`).

### Error "invalid address" en web UI
La imagen `cassandra-web` requiere una dirección IP, no un nombre de host. El `docker-compose.yml` ya asigna una IP estática (`172.20.0.10`) para evitar este problema.

### Error "Unknown column" al iniciar Cassandra
Ocurre al cambiar de versión de Cassandra con datos existentes. Solución:
```powershell
docker compose -f docker/docker-compose.yml down -v
docker compose -f docker/docker-compose.yml up -d
```
Esto borra el volumen de datos (¡cuidado! pierdes los datos existentes).

## Personalización

Para cambiar el nombre del cluster, edita en `docker/docker-compose.yml`:

```yaml
environment:
  - CASSANDRA_CLUSTER_NAME=TuNombreDeCluster
```

Para agregar tablas, modifica los archivos en la carpeta `scripts/` y reinicia con `down -v` + `up -d`.
