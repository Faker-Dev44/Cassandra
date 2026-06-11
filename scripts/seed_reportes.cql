USE museo_auditoria;

INSERT INTO reporte_facturacion_periodo (anio, mes, id_factura, fecha_emision, id_comprador, monto_neto, iva_calculado, ganancia_museo, estado)
VALUES (2025, 1, 1001, '2025-01-15', 101, 150.00, 24.00, 45.00, 'pagada');

INSERT INTO reporte_facturacion_periodo (anio, mes, id_factura, fecha_emision, id_comprador, monto_neto, iva_calculado, ganancia_museo, estado)
VALUES (2025, 1, 1002, '2025-01-20', 102, 280.50, 44.88, 84.15, 'pagada');

INSERT INTO reporte_facturacion_periodo (anio, mes, id_factura, fecha_emision, id_comprador, monto_neto, iva_calculado, ganancia_museo, estado)
VALUES (2025, 2, 1003, '2025-02-10', 101, 95.00, 15.20, 28.50, 'pagada');

INSERT INTO reporte_facturacion_periodo (anio, mes, id_factura, fecha_emision, id_comprador, monto_neto, iva_calculado, ganancia_museo, estado)
VALUES (2025, 2, 1004, '2025-02-25', 103, 420.00, 67.20, 126.00, 'pendiente');

INSERT INTO reporte_facturacion_periodo (anio, mes, id_factura, fecha_emision, id_comprador, monto_neto, iva_calculado, ganancia_museo, estado)
VALUES (2025, 3, 1005, '2025-03-05', 102, 310.00, 49.60, 93.00, 'pagada');

INSERT INTO reporte_facturacion_periodo (anio, mes, id_factura, fecha_emision, id_comprador, monto_neto, iva_calculado, ganancia_museo, estado)
VALUES (2025, 3, 1006, '2025-03-18', 101, 175.25, 28.04, 52.58, 'pagada');

INSERT INTO reporte_membresias_periodo (anio, mes, id_membresia, fecha_registro, id_comprador, codigo_membresia, monto_cobrado, estado)
VALUES (2025, 1, 2001, '2025-01-05', 101, 'MEM-2025-A001', 10.00, 'activa');

INSERT INTO reporte_membresias_periodo (anio, mes, id_membresia, fecha_registro, id_comprador, codigo_membresia, monto_cobrado, estado)
VALUES (2025, 1, 2002, '2025-01-12', 102, 'MEM-2025-A002', 10.00, 'activa');

INSERT INTO reporte_membresias_periodo (anio, mes, id_membresia, fecha_registro, id_comprador, codigo_membresia, monto_cobrado, estado)
VALUES (2025, 2, 2003, '2025-02-08', 101, 'MEM-2025-B001', 10.00, 'activa');

INSERT INTO reporte_membresias_periodo (anio, mes, id_membresia, fecha_registro, id_comprador, codigo_membresia, monto_cobrado, estado)
VALUES (2025, 2, 2004, '2025-02-20', 103, 'MEM-2025-B002', 10.00, 'vencida');

INSERT INTO reporte_membresias_periodo (anio, mes, id_membresia, fecha_registro, id_comprador, codigo_membresia, monto_cobrado, estado)
VALUES (2025, 3, 2005, '2025-03-01', 102, 'MEM-2025-C001', 10.00, 'activa');

INSERT INTO reporte_membresias_periodo (anio, mes, id_membresia, fecha_registro, id_comprador, codigo_membresia, monto_cobrado, estado)
VALUES (2025, 3, 2006, '2025-03-22', 101, 'MEM-2025-C002', 10.00, 'activa');
