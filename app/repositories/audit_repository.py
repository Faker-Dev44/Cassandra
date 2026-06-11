import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional
from cassandra import DriverException
from cassandra.cluster import NoHostAvailable, Session
from app.config.database import conexion_cassandra

logger = logging.getLogger("cassandra")


class BaseCassandraRepository(ABC):
    """
    Clase base para los repositorios de Cassandra.
    Maneja la lógica centralizada de conexión, reintentos y preparación de sentencias.
    """
    def __init__(self):
        self._inicializado = False

    @abstractmethod
    async def _preparar_sentencias(self, session: Session) -> None:
        """
        Método abstracto donde las clases hijas deben preparar sus sentencias CQL.
        """
        pass

    async def _asegurar_inicializacion(self, max_reintentos: int = 3, espera_segundos: int = 2):
        """
        Garantiza que la sesión esté activa y las sentencias preparadas.
        Implementa lógica de reintentos para robustez.
        """
        if self._inicializado:
            return

        for intento in range(1, max_reintentos + 1):
            try:
                session = conexion_cassandra.session
                if session is None:
                    logger.warning(f"[Cassandra] Intento {intento}: Sesión nula, reconectando...")
                    conexion_cassandra.conectar()
                    session = conexion_cassandra.session

                if session:
                    await self._preparar_sentencias(session)
                    self._inicializado = True
                    logger.info(f"[Cassandra] {self.__class__.__name__} inicializado con éxito.")
                    return
                else:
                    raise DriverException("No se pudo obtener una sesión válida de Cassandra.")

            except (NoHostAvailable, DriverException) as e:
                logger.error(
                    "Intento %d de %d fallido para %s: %s",
                    intento, max_reintentos, self.__class__.__name__, e
                )
                if intento == max_reintentos:
                    raise RuntimeError(f"Error crítico: No se pudo inicializar el repositorio {self.__class__.__name__}.") from e
                await asyncio.sleep(espera_segundos)
