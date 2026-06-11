import asyncio
import logging
from typing import List, Optional
from cassandra.cluster import Session
from cassandra.query import PreparedStatement

from app.config.database import conexion_cassandra
from app.schemas.reportes_schema import ReporteFacturacionSchema, ReporteMembresiaSchema
from app.repositories.audit_repository import BaseCassandraRepository

logger = logging.getLogger("cassandra")

class ReportesRepositorio(BaseCassandraRepository):
    def __init__(self):
        super().__init__()
        self._query_facturacion_prepared: Optional[PreparedStatement] = None
        self._query_membresias_prepared: Optional[PreparedStatement] = None
        self._insert_facturacion_prepared: Optional[PreparedStatement] = None
        self._insert_membresias_prepared: Optional[PreparedStatement] = None

    async def _preparar_sentencias(self, session: Session):
        self._query_facturacion_prepared = await asyncio.to_thread(
            session.prepare,
            "SELECT anio, mes, id_factura, fecha_emision, id_comprador, monto_neto, iva_calculado, ganancia_museo, estado "
            "FROM reporte_facturacion_periodo "
            "WHERE anio = ? AND mes = ?"
        )
        self._query_membresias_prepared = await asyncio.to_thread(
            session.prepare,
            "SELECT anio, mes, id_membresia, fecha_registro, id_comprador, codigo_membresia, monto_cobrado, estado "
            "FROM reporte_membresias_periodo "
            "WHERE anio = ? AND mes = ?"
        )
        self._insert_facturacion_prepared = await asyncio.to_thread(
            session.prepare,
            "INSERT INTO reporte_facturacion_periodo "
            "(anio, mes, id_factura, fecha_emision, id_comprador, monto_neto, iva_calculado, ganancia_museo, estado) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        self._insert_membresias_prepared = await asyncio.to_thread(
            session.prepare,
            "INSERT INTO reporte_membresias_periodo "
            "(anio, mes, id_membresia, fecha_registro, id_comprador, codigo_membresia, monto_cobrado, estado) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )

    async def insertar_factura(self, datos: ReporteFacturacionSchema):
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._insert_facturacion_prepared is not None

        await asyncio.to_thread(
            session.execute,
            self._insert_facturacion_prepared,
            (
                datos.anio,
                datos.mes,
                datos.id_factura,
                datos.fecha_emision,
                datos.id_comprador,
                datos.monto_neto,
                datos.iva_calculado,
                datos.ganancia_museo,
                datos.estado
            )
        )

    async def insertar_membresia(self, datos: ReporteMembresiaSchema):
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._insert_membresias_prepared is not None

        await asyncio.to_thread(
            session.execute,
            self._insert_membresias_prepared,
            (
                datos.anio,
                datos.mes,
                datos.id_membresia,
                datos.fecha_registro,
                datos.id_comprador,
                datos.codigo_membresia,
                datos.monto_cobrado,
                datos.estado
            )
        )

    async def obtener_reporte_facturacion(self, anio: int, mes: int) -> List[ReporteFacturacionSchema]:
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._query_facturacion_prepared is not None

        result = await asyncio.to_thread(
            session.execute,
            self._query_facturacion_prepared,
            (anio, mes)
        )

        return [
            ReporteFacturacionSchema(
                anio=row.anio,
                mes=row.mes,
                id_factura=row.id_factura,
                fecha_emision=row.fecha_emision,
                id_comprador=row.id_comprador,
                monto_neto=row.monto_neto,
                iva_calculado=row.iva_calculado,
                ganancia_museo=row.ganancia_museo,
                estado=row.estado
            )
            for row in result
        ]

    async def obtener_reporte_membresias(self, anio: int, mes: int) -> List[ReporteMembresiaSchema]:
        await self._asegurar_inicializacion()
        session = conexion_cassandra.session
        assert session is not None
        assert self._query_membresias_prepared is not None

        result = await asyncio.to_thread(
            session.execute,
            self._query_membresias_prepared,
            (anio, mes)
        )

        return [
            ReporteMembresiaSchema(
                anio=row.anio,
                mes=row.mes,
                id_membresia=row.id_membresia,
                fecha_registro=row.fecha_registro,
                id_comprador=row.id_comprador,
                codigo_membresia=row.codigo_membresia,
                monto_cobrado=row.monto_cobrado,
                estado=row.estado
            )
            for row in result
        ]
