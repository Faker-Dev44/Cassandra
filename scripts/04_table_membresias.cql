USE museo_auditoria;

CREATE TABLE IF NOT EXISTS auditoria_codigos_membresia (
    id_comprador int,
    fecha_registro timestamp,
    codigo_seguridad text,
    correo_envio text,
    estado text,
    PRIMARY KEY ((id_comprador), fecha_registro)
) WITH CLUSTERING ORDER BY (fecha_registro DESC);
