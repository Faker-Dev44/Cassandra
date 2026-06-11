from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional


class AuditBaseSchema(BaseModel):
    """
    Clase base global para el control de auditoría del museo.
    Todos los esquemas específicos (Obras, Seguridad, Reportes)
    heredarán estos metadatos obligatorios para garantizar la trazabilidad.
    """
    
    usuario_id: int = Field(
        ..., 
        description="ID del usuario responsable de la acción en el Core SQL",
        examples=[1]
    )

    fecha_evento: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha y hora exacta en la que ocurrió el evento (Formato ISO/UTC)"
    )

    ip_origen: Optional[str] = Field(
        default="127.0.0.1",
        description="Dirección IP desde la cual se realizó la petición",
        examples=["192.168.1.50"]
    )

    model_config = {
        "frozen": True,
        "json_schema_extra": {
            "example": {
                "usuario_id": 1,
                "fecha_evento": "2026-05-31T18:45:00Z",
                "ip_origen": "127.0.0.1"
            }
        }
    }