USE museo_auditoria;

-- Simulación de ciclo de vida para la Obra 1001 (Disponible -> Reservada -> Vendida)
INSERT INTO historico_estatus_obras (id_obra, fecha_evento, estatus_anterior, estatus_nuevo, usuario_id, ip_origen)
VALUES (1001, '2026-06-01 09:00:00', 'Creada', 'Disponible', 10, '192.168.1.50');

INSERT INTO historico_estatus_obras (id_obra, fecha_evento, estatus_anterior, estatus_nuevo, usuario_id, ip_origen)
VALUES (1001, '2026-06-02 14:30:00', 'Disponible', 'Reservada', 12, '192.168.1.55');

INSERT INTO historico_estatus_obras (id_obra, fecha_evento, estatus_anterior, estatus_nuevo, usuario_id, ip_origen)
VALUES (1001, '2026-06-03 11:15:00', 'Reservada', 'Vendida', 10, '192.168.1.50');


-- Simulación de ciclo de vida para la Obra 1002 (Disponible -> Reservada -> Disponible por cancelación)
INSERT INTO historico_estatus_obras (id_obra, fecha_evento, estatus_anterior, estatus_nuevo, usuario_id, ip_origen)
VALUES (1002, '2026-06-01 10:00:00', 'Creada', 'Disponible', 10, '192.168.1.50');

INSERT INTO historico_estatus_obras (id_obra, fecha_evento, estatus_anterior, estatus_nuevo, usuario_id, ip_origen)
VALUES (1002, '2026-06-02 16:00:00', 'Disponible', 'Reservada', 15, '192.168.1.60');

INSERT INTO historico_estatus_obras (id_obra, fecha_evento, estatus_anterior, estatus_nuevo, usuario_id, ip_origen)
VALUES (1002, '2026-06-03 09:00:00', 'Reservada', 'Disponible', 10, '192.168.1.50');