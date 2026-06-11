from fastapi import APIRouter, HTTPException, Path, status
from typing import List

from app.repositories.obras_repository import ObrasRepositorio
from app.schemas.obras_schema import ObrasSchema

router = APIRouter(prefix="/obras", tags=["Obras"])
repo = ObrasRepositorio()


@router.post(
    "/historico",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Registrar un evento de cambio de estatus en una obra"
)
async def registrar_evento(datos: ObrasSchema):
    try:
        await repo.registrar_cambio_estatus(datos)
        return {"mensaje": "Historial de cambio de estatus registrado con éxito"}
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )


@router.get(
    "/historico/{id_obra}",
    response_model=List[ObrasSchema],
    summary="Obtener historial de cambios de estatus de una obra (Administrador)"
)
async def obtener_historial_obra(
    id_obra: int = Path(..., description="ID numérico de la obra de arte", example=1001)
):
    try:
        resultados = await repo.obtener_historial(id_obra)
        if not resultados:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron registros de auditoría para la obra con ID {id_obra}"
            )
        return resultados
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )