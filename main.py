from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.config.database import conexion_cassandra
from app.routes.membresias_routes import router as membresias_router
from app.routes.seguridad_routes import router as seguridad_router
from app.routes.obras_routes import router as obras_routes
from app.routes.reportes_routes import router as reportes_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    conexion_cassandra.conectar()
    yield
    conexion_cassandra.cerrar()

app = FastAPI(
    title="Museo Atrium - Microservicio de Auditoría (Cassandra)",
    version="1.0.0",
    lifespan=lifespan
)


@app.exception_handler(RequestValidationError)
async def validacion_erronea_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

@app.get("/health", tags=["Salud"])
async def health_check():
    return {"status": "healthy", "service": "Cassandra Audit Service"}

app.include_router(seguridad_router)
app.include_router(obras_routes)
app.include_router(membresias_router)
app.include_router(reportes_router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Microservicio de Auditoría del Museo en funcionamiento"}

# Agregar en el microservicio de Cassandra (Python - FastAPI):
from app.config.database import conexion_cassandra

@app.get("/ping-db", tags=["Salud"])
async def ping_database():
    try:
        session = conexion_cassandra.session
        if session is None:
            # Intentar reconectar si la sesión se había cerrado
            conexion_cassandra.conectar()
            session = conexion_cassandra.session
            
        if session:
            # Ejecuta la consulta de metadatos más rápida y ligera de Cassandra
            row = session.execute("SELECT release_version FROM system.local").one()
            return {
                "status": "online",
                "cassandra_version": row[0],
                "message": "Astra DB despertado con éxito"
            }
        return {"status": "error", "message": "Sesión de Cassandra no disponible"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


import uvicorn
import os

if __name__ == "__main__":
    # Render asigna automáticamente un puerto dinámico en la variable PORT
    port = int(os.getenv("PORT", 8080))
    
    # En producción DEBE ser 0.0.0.0 para escuchar conexiones externas
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)