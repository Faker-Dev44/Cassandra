from typing import Optional

from fastapi import APIRouter, Query

from app.repositories.membresias_repository import MembresiasRepositorio
from app.schemas.membresias_schema import (
    CodigoMembresiaSchema,
    PaginaCodigoMembresiaSchema,
)

router = APIRouter(prefix="/membresias", tags=["Membresias"])
repo = MembresiasRepositorio()


@router.post(
    "/codigos",
    status_code=201,
    responses={
        201: {"description": "Codigo de membresia creado correctamente"},
        400: {"description": "Error de validacion"},
    },
)
async def crear_codigo(datos: CodigoMembresiaSchema):
    registro = await repo.insertar_codigo(datos)
    return {"mensaje": "Codigo de membresia insertado", "datos": registro}


@router.get("/codigos", response_model=PaginaCodigoMembresiaSchema)
async def consultar_codigos(
    id_comprador: int = Query(..., description="Identificador del comprador"),
    page_size: int = Query(20, ge=1, le=100, description="Tamano de pagina para la lectura"),
    paging_state: Optional[str] = Query(None, description="Token base64 devuelto por la pagina anterior"),
):
    registros, siguiente_paging_state = await repo.obtener_codigos_por_comprador(
        id_comprador=id_comprador,
        page_size=page_size,
        paging_state=paging_state,
    )
    return {"datos": registros, "paging_state": siguiente_paging_state}
