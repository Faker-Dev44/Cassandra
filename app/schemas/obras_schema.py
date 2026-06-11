from pydantic import Field
from app.schemas.audit_schemas import AuditBaseSchema


class ObrasSchema(AuditBaseSchema):
    """
    Esquema de validación para registrar y consultar cambios de estado en las obras.
    Hereda ip_origen, fecha_evento y usuario_id de AuditBaseSchema.
    """
    id_obra: int = Field(
        ...,
        description="ID de la obra de arte afectada",
        examples=[1001]
    )
    estatus_anterior: str = Field(
        ...,
        description="Estatus previo de la obra (ej. Disponible, Reservada)",
        examples=["Disponible"]
    )
    estatus_nuevo: str = Field(
        ...,
        description="Nuevo estatus asignado a la obra (ej. Reservada, Vendida)",
        examples=["Reservada"]
    )

    model_config = {
        "frozen": True,
        "json_schema_extra": {
            "example": {
                "id_obra": 1001,
                "estatus_anterior": "Disponible",
                "estatus_nuevo": "Reservada",
                "usuario_id": 12,
                "fecha_evento": "2026-06-02T14:30:00Z",
                "ip_origen": "192.168.1.55"
            }
        }
    }