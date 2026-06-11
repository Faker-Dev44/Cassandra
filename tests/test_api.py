import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timezone
from typing import Optional

from main import app
from app.schemas.obras_schema import ObrasSchema
from app.schemas.seguridad_schema import SeguridadSchema
from app.schemas.membresias_schema import CodigoMembresiaSchema
from app.schemas.reportes_schema import ReporteFacturacionSchema, ReporteMembresiaSchema

COMPRADOR_TEST = 500

@pytest.fixture
def mock_reportes_repo(monkeypatch):
    class MockReportesRepositorio:
        async def insertar_factura(self, datos):
            pass
        
        async def insertar_membresia(self, datos):
            pass

        async def obtener_reporte_facturacion(self, anio: int, mes: int):
            if anio == 2025 and mes == 1:
                return [
                    ReporteFacturacionSchema(
                        anio=2025,
                        mes=1,
                        id_factura=1001,
                        fecha_emision=datetime.now(timezone.utc),
                        id_comprador=101,
                        monto_neto=150.0,
                        iva_calculado=24.0,
                        ganancia_museo=45.0,
                        estado="pagada"
                    )
                ]
            return []

        async def obtener_reporte_membresias(self, anio: int, mes: int):
            if anio == 2025 and mes == 1:
                return [
                    ReporteMembresiaSchema(
                        anio=2025,
                        mes=1,
                        id_membresia=2001,
                        fecha_registro=datetime.now(timezone.utc),
                        id_comprador=101,
                        codigo_membresia="MEM-2025-A001",
                        monto_cobrado=10.0,
                        estado="activa"
                    )
                ]
            return []

    monkeypatch.setattr("app.routes.reportes_routes.repo", MockReportesRepositorio())

@pytest.fixture
def mock_obras_repo(monkeypatch):
    class MockObrasRepositorio:
        async def registrar_cambio_estatus(self, datos):
            pass
        
        async def obtener_historial(self, id_obra: int):
            if id_obra == 1001:
                return [
                    ObrasSchema(
                        id_obra=1001,
                        fecha_evento=datetime.now(timezone.utc),
                        estatus_anterior="Disponible",
                        estatus_nuevo="Reservada",
                        usuario_id=1,
                        ip_origen="192.168.1.10"
                    )
                ]
            return []
    
    monkeypatch.setattr("app.routes.obras_routes.repo", MockObrasRepositorio())

@pytest.fixture
def mock_seguridad_repo(monkeypatch):
    class MockSeguridadRepositorio:
        async def insertar_log(self, datos):
            pass
            
        async def obtener_logs_por_usuario(self, login_usuario: str, desde: datetime, hasta: datetime):
            if login_usuario == "admin":
                return [
                    SeguridadSchema(
                        login_usuario="admin",
                        fecha_evento=datetime.now(timezone.utc),
                        evento_tipo="LOGIN_EXITOSO",
                        ip_origen="192.168.1.10",
                        detalles="Ingreso al sistema",
                        usuario_id=1
                    )
                ]
            return []

    monkeypatch.setattr("app.routes.seguridad_routes.repo", MockSeguridadRepositorio())

@pytest.fixture
def mock_membresias_repo(monkeypatch):
    class MockMembresiasRepositorio:
        async def insertar_codigo(self, datos):
            return datos
        
        async def obtener_codigos_por_comprador(self, id_comprador: int, page_size: int = 20, paging_state: Optional[str] = None):
            if id_comprador == COMPRADOR_TEST:
                return [
                    CodigoMembresiaSchema(
                        id_comprador=COMPRADOR_TEST,
                        fecha_registro=datetime.now(timezone.utc),
                        codigo_seguridad="SECRET123",
                        correo_envio="test@example.com",
                        estado="EMITIDO"
                    )
                ], None
            return [], None

    monkeypatch.setattr("app.routes.membresias_routes.repo", MockMembresiasRepositorio())

@pytest.mark.asyncio
async def test_registrar_evento_obra(mock_obras_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "id_obra": 1001,
            "fecha_evento": datetime.now(timezone.utc).isoformat(),
            "estatus_anterior": "Disponible",
            "estatus_nuevo": "Reservada",
            "usuario_id": 1,
            "ip_origen": "192.168.1.10"
        }
        response = await client.post("/obras/historico", json=payload)
        assert response.status_code == 201
        assert response.json() == {"mensaje": "Historial de cambio de estatus registrado con éxito"}

@pytest.mark.asyncio
async def test_obtener_historial_obra(mock_obras_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/obras/historico/1001")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id_obra"] == 1001
        assert data[0]["estatus_nuevo"] == "Reservada"

@pytest.mark.asyncio
async def test_obtener_historial_obra_no_encontrada(mock_obras_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/obras/historico/9999")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_registrar_log_seguridad(mock_seguridad_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "login_usuario": "admin",
            "fecha_evento": datetime.now(timezone.utc).isoformat(),
            "evento_tipo": "LOGIN_EXITOSO",
            "ip_origen": "192.168.1.10",
            "detalles": "Ingreso al sistema",
            "usuario_id": 1
        }
        response = await client.post("/seguridad/logs", json=payload)
        assert response.status_code == 201

@pytest.mark.asyncio
async def test_obtener_logs_seguridad(mock_seguridad_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/seguridad/logs?login_usuario=admin&desde=2023-01-01T00:00:00Z&hasta=2024-12-31T23:59:59Z")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["login_usuario"] == "admin"

@pytest.mark.asyncio
async def test_registrar_codigo_membresia(mock_membresias_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "id_comprador": COMPRADOR_TEST,
            "fecha_registro": datetime.now(timezone.utc).isoformat(),
            "codigo_seguridad": "SECRET123",
            "correo_envio": "test@example.com",
            "estado": "EMITIDO"
        }
        response = await client.post("/membresias/codigos", json=payload)
        assert response.status_code == 201
        assert response.json()["mensaje"] == "Codigo de membresia insertado"

@pytest.mark.asyncio
async def test_obtener_codigos_membresia(mock_membresias_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/membresias/codigos?id_comprador={COMPRADOR_TEST}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["datos"]) == 1
        assert data["datos"][0]["id_comprador"] == COMPRADOR_TEST

@pytest.mark.asyncio
async def test_obtener_reporte_facturacion(mock_reportes_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/reportes/facturacion?anio=2025&mes=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["anio"] == 2025
        assert data[0]["mes"] == 1
        assert data[0]["id_comprador"] == 101

@pytest.mark.asyncio
async def test_obtener_reporte_membresias(mock_reportes_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/reportes/membresias?anio=2025&mes=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["anio"] == 2025
        assert data[0]["mes"] == 1
        assert data[0]["codigo_membresia"] == "MEM-2025-A001"

@pytest.mark.asyncio
async def test_post_reporte_facturacion(mock_reportes_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "anio": 2025,
            "mes": 1,
            "id_factura": 1001,
            "fecha_emision": datetime.now(timezone.utc).isoformat(),
            "id_comprador": 101,
            "monto_neto": 150.0,
            "iva_calculado": 24.0,
            "ganancia_museo": 45.0,
            "estado": "pagada"
        }
        response = await client.post("/reportes/facturacion", json=payload)
        assert response.status_code == 201
        assert response.json()["mensaje"] == "Reporte de facturación insertado correctamente"

@pytest.mark.asyncio
async def test_post_reporte_membresia(mock_reportes_repo):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "anio": 2025,
            "mes": 1,
            "id_membresia": 2001,
            "fecha_registro": datetime.now(timezone.utc).isoformat(),
            "id_comprador": 101,
            "codigo_membresia": "MEM-2025-A001",
            "monto_cobrado": 10.0,
            "estado": "activa"
        }
        response = await client.post("/reportes/membresias", json=payload)
        assert response.status_code == 201
        assert response.json()["mensaje"] == "Reporte de membresía insertado correctamente"

