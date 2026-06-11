import asyncio
import base64
import logging
from typing import List, Optional, Tuple
from cassandra.cluster import Session
from cassandra.query import PreparedStatement

from app.config.database import conexion_cassandra
from app.schemas.membresias_schema import CodigoMembresiaSchema, EstadoCodigoMembresia
from app.repositories.audit_repository import BaseCassandraRepository

logger = logging.getLogger("cassandra")

class MembresiasRepositorio(BaseCassandraRepository):
    def __init__(self):
        super().__init__()
        self._insert_prepared: Optional[PreparedStatement] = None
        self._query_prepared: Optional[PreparedStatement] = None

    async def _preparar_sentencias(self, session: Session):
        """
        Prepara las sentencias de Cassandra específicas para el módulo de Membresías.
        """
        self._insert_prepared = await asyncio.to_thread(
            session.prepare,
            "INSERT INTO auditoria_codigos_membresia "
            "(id_comprador, fecha_registro, codigo_seguridad, correo_envio, estado) "
            "VALUES (?, ?, ?, ?, ?)"
        )
        self._query_prepared = await asyncio.to_thread(
            session.prepare,
            "SELECT id_comprador, fecha_registro, codigo_seguridad, correo_envio, estado "
            "FROM auditoria_codigos_membresia "
            "WHERE id_comprador = ?"
        )

    async def insertar_codigo(self, datos: CodigoMembresiaSchema) -> CodigoMembresiaSchema:
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._insert_prepared is not None

        await asyncio.to_thread(
            session.execute,
            self._insert_prepared,
            (
                datos.id_comprador,
                datos.fecha_registro,
                datos.codigo_seguridad,
                str(datos.correo_envio),
                datos.estado.value if isinstance(datos.estado, EstadoCodigoMembresia) else str(datos.estado),
            ),
        )
        return datos

    async def obtener_codigos_por_comprador(
        self,
        id_comprador: int,
        page_size: int = 20,
        paging_state: Optional[str] = None,
    ) -> Tuple[List[CodigoMembresiaSchema], Optional[str]]:
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._query_prepared is not None

        paging_state_bytes = base64.b64decode(paging_state) if paging_state else None
        consulta = self._query_prepared.bind((id_comprador,))
        consulta.fetch_size = page_size

        result = await asyncio.to_thread(
            session.execute,
            consulta,
            paging_state=paging_state_bytes,
        )

        registros: List[CodigoMembresiaSchema] = [
            CodigoMembresiaSchema(
                id_comprador=row.id_comprador,
                fecha_registro=row.fecha_registro,
                codigo_seguridad=row.codigo_seguridad,
                correo_envio=row.correo_envio,
                estado=row.estado,
            )
            for row in result
        ]

        siguiente_paging_state = None
        if getattr(result, "has_more_pages", False) and getattr(result, "paging_state", None):
            siguiente_paging_state = base64.b64encode(result.paging_state).decode("utf-8")

        return registros, siguiente_paging_state
