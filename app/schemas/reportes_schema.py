from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field

class ReporteFacturacionSchema(BaseModel):
    anio: int
    mes: int
    id_factura: int
    fecha_emision: datetime
    id_comprador: int
    monto_neto: Decimal
    iva_calculado: Decimal
    ganancia_museo: Decimal
    estado: str

    model_config = {
        "from_attributes": True
    }

class ReporteMembresiaSchema(BaseModel):
    anio: int
    mes: int
    id_membresia: int
    fecha_registro: datetime
    id_comprador: int
    codigo_membresia: str
    monto_cobrado: Decimal
    estado: str

    model_config = {
        "from_attributes": True
    }

class FiltroReporteSchema(BaseModel):
    anio: int = Field(..., ge=2020, le=2100)
    mes: int = Field(..., ge=1, le=12)
