import asyncio
import logging
from typing import List, Optional
from cassandra import DriverException
from cassandra.cluster import Session
from cassandra.query import PreparedStatement

from app.config.database import conexion_cassandra
from app.schemas.obras_schema import ObrasSchema
from app.repositories.audit_repository import BaseCassandraRepository

logger = logging.getLogger("cassandra")


class ObrasRepositorio(BaseCassandraRepository):
    def __init__(self):
        super().__init__()
        self._insert_prepared: Optional[PreparedStatement] = None
        self._query_por_obra: Optional[PreparedStatement] = None

    async def _preparar_sentencias(self, session: Session) -> None:
        """
        Prepara las sentencias de Cassandra específicas para el módulo de Obras.
        """
        self._insert_prepared = await asyncio.to_thread(
            session.prepare,
            "INSERT INTO historico_estatus_obras "
            "(id_obra, fecha_evento, estatus_anterior, estatus_nuevo, usuario_id, ip_origen) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )

        self._query_por_obra = await asyncio.to_thread(
            session.prepare,
            "SELECT id_obra, fecha_evento, estatus_anterior, estatus_nuevo, usuario_id, ip_origen "
            "FROM historico_estatus_obras "
            "WHERE id_obra = ?"
        )

    async def registrar_cambio_estatus(self, datos: ObrasSchema) -> None:
        """
        Inserta un evento de auditoría de cambio de estado en Cassandra.
        """
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._insert_prepared is not None

        try:
            await asyncio.to_thread(
                session.execute,
                self._insert_prepared,
                (
                    datos.id_obra,
                    datos.fecha_evento,
                    datos.estatus_anterior,
                    datos.estatus_nuevo,
                    datos.usuario_id,
                    datos.ip_origen
                )
            )
            logger.info(
                "Historial de obra registrado: id_obra=%d, nuevo_estatus=%s",
                datos.id_obra, datos.estatus_nuevo
            )
        except DriverException as e:
            logger.error("Error del driver de Cassandra al insertar historial de obra: %s", e)
            raise RuntimeError("Fallo en la base de datos de auditoría al insertar registro.") from e

    async def obtener_historial(self, id_obra: int) -> List[ObrasSchema]:
        """
        Retorna el histórico de cambios de estado para una obra específica.
        """
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._query_por_obra is not None

        try:
            rows = await asyncio.to_thread(
                session.execute,
                self._query_por_obra,
                (id_obra,)
            )

            resultados: List[ObrasSchema] = [
                ObrasSchema(
                    id_obra=row.id_obra,
                    fecha_evento=row.fecha_evento,
                    estatus_anterior=row.estatus_anterior,
                    estatus_nuevo=row.estatus_nuevo,
                    usuario_id=row.usuario_id,
                    ip_origen=row.ip_origen
                )
                for row in rows
            ]
            logger.info("Consulta exitosa: id_obra=%d, total_registros=%d", id_obra, len(resultados))
            return resultados

        except DriverException as e:
            logger.error("Error del driver de Cassandra al consultar historial de obra %d: %s", id_obra, e)
            raise RuntimeError("Fallo en la base de datos de auditoría al recuperar historial.") from e
