USE museo_auditoria;

CREATE TABLE IF NOT EXISTS reporte_facturacion_periodo (
    anio int,
    mes int,
    id_factura int,
    fecha_emision timestamp,
    id_comprador int,
    monto_neto decimal,
    iva_calculado decimal,
    ganancia_museo decimal,
    estado text,
    PRIMARY KEY ((anio, mes), fecha_emision, id_factura)
) WITH CLUSTERING ORDER BY (fecha_emision DESC, id_factura ASC);

CREATE TABLE IF NOT EXISTS reporte_membresias_periodo (
    anio int,
    mes int,
    id_membresia int,
    fecha_registro timestamp,
    id_comprador int,
    codigo_membresia text,
    monto_cobrado decimal,
    estado text,
    PRIMARY KEY ((anio, mes), fecha_registro, id_membresia)
) WITH CLUSTERING ORDER BY (fecha_registro DESC, id_membresia ASC);
