import asyncio
import logging
from datetime import datetime
from typing import List, Optional
from cassandra.cluster import Session
from cassandra.query import PreparedStatement
from app.config.database import conexion_cassandra
from app.schemas.seguridad_schema import SeguridadSchema
from app.repositories.audit_repository import BaseCassandraRepository

logger = logging.getLogger("cassandra")


class SeguridadRepositorio(BaseCassandraRepository):
    def __init__(self):
        super().__init__()
        self._insert_prepared: Optional[PreparedStatement] = None
        self._query_por_usuario: Optional[PreparedStatement] = None

    async def _preparar_sentencias(self, session: Session) -> None:
        """
        Prepara las sentencias de Cassandra específicas para el módulo de Seguridad.
        """
        self._insert_prepared = await asyncio.to_thread(
            session.prepare,
            "INSERT INTO bitacora_seguridad "
            "(login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id) "
            "VALUES (?, ?, ?, ?, ?, ?)"
        )
        self._query_por_usuario = await asyncio.to_thread(
            session.prepare,
            "SELECT login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id "
            "FROM bitacora_seguridad "
            "WHERE login_usuario = ? AND fecha_evento >= ? AND fecha_evento <= ? "
            "ORDER BY fecha_evento ASC"
        )

    async def insertar_log(self, datos: SeguridadSchema) -> None:
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._insert_prepared is not None
        try:
            await asyncio.to_thread(
                session.execute,
                self._insert_prepared,
                (
                    datos.login_usuario,
                    datos.fecha_evento,
                    datos.evento_tipo,
                    datos.ip_origen,
                    datos.detalles,
                    datos.usuario_id,
                ),
            )
            logger.info(
                "Log de seguridad insertado: login=%s, evento=%s, ip=%s",
                datos.login_usuario,
                datos.evento_tipo,
                datos.ip_origen,
            )
        except Exception as e:
            logger.error(
                "Error al insertar log de seguridad: login=%s, evento=%s, error=%s",
                datos.login_usuario,
                datos.evento_tipo,
                e,
            )
            raise

    async def obtener_logs_por_usuario(
        self,
        login_usuario: str,
        desde: datetime,
        hasta: datetime,
    ) -> List[SeguridadSchema]:
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._query_por_usuario is not None
        try:
            rows = await asyncio.to_thread(
                session.execute,
                self._query_por_usuario,
                (login_usuario, desde, hasta),
            )
            resultados: List[SeguridadSchema] = [
                SeguridadSchema(
                    login_usuario=row.login_usuario,
                    fecha_evento=row.fecha_evento,
                    evento_tipo=row.accion,
                    ip_origen=row.ip_origen,
                    detalles=row.detalles,
                    usuario_id=row.usuario_id,
                )
                for row in rows
            ]
            logger.info(
                "Logs consultados: usuario=%s, desde=%s, hasta=%s, total=%d",
                login_usuario, desde, hasta, len(resultados),
            )
            return resultados
        except Exception as e:
            logger.error(
                "Error al consultar logs de seguridad: usuario=%s, error=%s",
                login_usuario, e,
            )
            raise
