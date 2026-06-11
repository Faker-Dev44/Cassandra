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

if __name__ == "__main__":
    import uvicorn

    # Aquí puedes cambiar el 8080 por el puerto que necesites
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)