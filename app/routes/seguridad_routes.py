from datetime import datetime
from fastapi import APIRouter, Query

from app.repositories.seguridad_repository import SeguridadRepositorio
from app.schemas.seguridad_schema import SeguridadSchema

router = APIRouter(prefix="/seguridad", tags=["Seguridad"])
repo = SeguridadRepositorio()


@router.post("/logs", status_code=201)
async def crear_log(datos: SeguridadSchema):
    await repo.insertar_log(datos)
    return {"mensaje": "Log de seguridad insertado", "datos": datos}


@router.get("/logs")
async def consultar_logs(
    login_usuario: str = Query(..., description="Nombre de usuario"),
    desde: datetime = Query(..., description="Inicio del rango (ISO 8601)"),
    hasta: datetime = Query(..., description="Fin del rango (ISO 8601)"),
):
    resultados = await repo.obtener_logs_por_usuario(
        login_usuario, desde, hasta
    )
    return resultados
