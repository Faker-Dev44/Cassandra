from typing import List
from fastapi import APIRouter, Query, HTTPException

from app.repositories.reportes_repository import ReportesRepositorio
from app.schemas.reportes_schema import ReporteFacturacionSchema, ReporteMembresiaSchema

router = APIRouter(prefix="/reportes", tags=["Reportes"])
repo = ReportesRepositorio()

@router.get("/facturacion", response_model=List[ReporteFacturacionSchema])
async def get_reporte_facturacion(
    anio: int = Query(..., ge=2020, le=2100),
    mes: int = Query(..., ge=1, le=12)
):
    try:
        return await repo.obtener_reporte_facturacion(anio, mes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facturacion", status_code=201)
async def post_reporte_facturacion(datos: ReporteFacturacionSchema):
    try:
        await repo.insertar_factura(datos)
        return {"mensaje": "Reporte de facturación insertado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/membresias", response_model=List[ReporteMembresiaSchema])
async def get_reporte_membresias(
    anio: int = Query(..., ge=2020, le=2100),
    mes: int = Query(..., ge=1, le=12)
):
    try:
        return await repo.obtener_reporte_membresias(anio, mes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/membresias", status_code=201)
async def post_reporte_membresia(datos: ReporteMembresiaSchema):
    try:
        await repo.insertar_membresia(datos)
        return {"mensaje": "Reporte de membresía insertado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
