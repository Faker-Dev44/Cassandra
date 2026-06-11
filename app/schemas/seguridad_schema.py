from enum import Enum
from typing import Optional
from pydantic import Field, field_validator
from app.schemas.audit_schemas import AuditBaseSchema


class SeguridadEvento(str, Enum):
    LOGIN_EXITOSO = "LOGIN_EXITOSO"
    LOGIN_FALLIDO = "LOGIN_FALLIDO"


class SeguridadSchema(AuditBaseSchema):
    login_usuario: str = Field(
        ...,
        description="Nombre de usuario que intenta acceder al sistema",
        examples=["jperez"]
    )

    evento_tipo: SeguridadEvento = Field(
        ...,
        description="Tipo de evento de seguridad (LOGIN_EXITOSO, LOGIN_FALLIDO)",
        examples=["LOGIN_EXITOSO"]
    )

    @field_validator("evento_tipo", mode="before")
    @classmethod
    def upper_evento(cls, v: str) -> str:
        return v.upper()

    detalles: Optional[str] = Field(
        default=None,
        description="Detalles adicionales del evento de seguridad",
        examples=["Contrasena incorrecta", "Bloqueo por multiples intentos fallidos"]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "usuario_id": 1,
                "fecha_evento": "2026-06-01T08:15:00Z",
                "ip_origen": "192.168.1.10",
                "login_usuario": "jperez",
                "evento_tipo": "LOGIN_EXITOSO",
                "detalles": "Inicio de sesion exitoso"
            }
        }
    }
