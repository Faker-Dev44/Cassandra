USE museo_auditoria;

CREATE TABLE IF NOT EXISTS bitacora_seguridad (
    login_usuario text,
    fecha_evento timestamp,
    accion text,
    ip_origen text,
    detalles text,
    usuario_id int,
    PRIMARY KEY ((login_usuario), fecha_evento)
) WITH CLUSTERING ORDER BY (fecha_evento ASC);
