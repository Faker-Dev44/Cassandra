USE museo_auditoria;

CREATE TABLE IF NOT EXISTS historico_estatus_obras (
    id_obra int,
    fecha_evento timestamp,
    estatus_anterior text,
    estatus_nuevo text,
    usuario_id int,
    ip_origen text,
    PRIMARY KEY ((id_obra), fecha_evento)
) WITH CLUSTERING ORDER BY (fecha_evento DESC);