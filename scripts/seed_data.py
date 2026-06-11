import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cassandra.cluster import Cluster

KEYSPACE = "museo_auditoria"

TABLAS = f"""
CREATE TABLE IF NOT EXISTS {KEYSPACE}.bitacora_seguridad (
    login_usuario text,
    fecha_evento timestamp,
    accion text,
    ip_origen text,
    detalles text,
    usuario_id int,
    PRIMARY KEY ((login_usuario), fecha_evento)
) WITH CLUSTERING ORDER BY (fecha_evento ASC);

CREATE TABLE IF NOT EXISTS {KEYSPACE}.auditoria_codigos_membresia (
    id_comprador int,
    fecha_registro timestamp,
    codigo_seguridad text,
    correo_envio text,
    estado text,
    PRIMARY KEY ((id_comprador), fecha_registro)
) WITH CLUSTERING ORDER BY (fecha_registro DESC);
"""

COMPRADOR_1 = 1
COMPRADOR_2 = 2
COMPRADOR_3 = 3

SEED_MEMBRESIAS = [
    (COMPRADOR_1, datetime(2026, 6, 4, 8, 0, 0), 'MK8X2Q9Z', 'comprador1@correo.com', 'EMITIDO'),
    (COMPRADOR_1, datetime(2026, 6, 4, 10, 15, 0), 'Q7LM2V8P', 'comprador1@correo.com', 'EMITIDO'),
    (COMPRADOR_2, datetime(2026, 6, 4, 9, 30, 0), 'A9T4N6K1', 'comprador2@correo.com', 'EMITIDO'),
    (COMPRADOR_3, datetime(2026, 6, 4, 11, 45, 0), 'X3C9R2HF', 'comprador3@correo.com', 'EMITIDO'),
    (COMPRADOR_3, datetime(2026, 6, 4, 12, 5, 0), 'L5V8Q1MN', 'comprador3@correo.com', 'EMITIDO'),
]

INSERT_MEMBRESIA = f"""
    INSERT INTO {KEYSPACE}.auditoria_codigos_membresia
    (id_comprador, fecha_registro, codigo_seguridad, correo_envio, estado)
    VALUES (?, ?, ?, ?, ?)
"""


def seed():
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()

    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
    """)
    session.set_keyspace(KEYSPACE)
    print(f"[OK] Keyspace '{KEYSPACE}' listo")

    for stmt in TABLAS.split(';'):
        stmt = stmt.strip()
        if stmt:
            session.execute(stmt + ';')
    print("[OK] Tablas creadas/verificadas")

    prepared = session.prepare(INSERT_MEMBRESIA)
    for datos in SEED_MEMBRESIAS:
        session.execute(prepared, datos)
        print(f"  Insertado: comprador {datos[0]} - código {datos[2]}")

    print(f"\n[OK] {len(SEED_MEMBRESIAS)} registros insertados en auditoria_codigos_membresia")
    session.shutdown()
    cluster.shutdown()


if __name__ == "__main__":
    seed()
    input("Presiona Enter para salir...")
