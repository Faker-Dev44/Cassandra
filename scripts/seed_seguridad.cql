USE museo_auditoria;

-- ============================================================
-- INSERCIONES DE PRUEBA - BITACORA DE SEGURIDAD
-- ============================================================
-- jperez: inicios de sesión exitosos + 1 fallido
-- ============================================================

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('jperez', '2026-06-01 08:15:00', 'LOGIN_EXITOSO', '192.168.1.10', 'Inicio de sesion exitoso', 101);

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('jperez', '2026-06-01 12:30:00', 'LOGIN_EXITOSO', '192.168.1.10', 'Inicio de sesion exitoso', 101);

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('jperez', '2026-06-02 07:45:00', 'LOGIN_FALLIDO', '192.168.1.20', 'Contrasena incorrecta', 101);

-- ============================================================
-- mgonzalez: 2 intentos fallidos + 1 exitoso
-- ============================================================

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('mgonzalez', '2026-06-01 09:00:00', 'LOGIN_FALLIDO', '10.0.0.45', 'Usuario no encontrado', 102);

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('mgonzalez', '2026-06-01 09:01:00', 'LOGIN_FALLIDO', '10.0.0.45', 'Contrasena incorrecta', 102);

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('mgonzalez', '2026-06-01 09:02:00', 'LOGIN_EXITOSO', '10.0.0.45', 'Inicio de sesion exitoso tras 2 intentos', 102);

-- ============================================================
-- lrodriguez: 1 exitoso + 1 fallido por sesion expirada
-- ============================================================

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('lrodriguez', '2026-06-01 10:00:00', 'LOGIN_EXITOSO', '172.16.0.8', 'Inicio de sesion exitoso', 103);

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('lrodriguez', '2026-06-02 14:30:00', 'LOGIN_FALLIDO', '172.16.0.8', 'Sesion expirada', 103);

-- ============================================================
-- amartinez: 3 fallidos (bloqueo) + 1 exitoso post-desbloqueo
-- ============================================================

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('amartinez', '2026-06-01 11:00:00', 'LOGIN_FALLIDO', '192.168.5.100', 'Contrasena incorrecta', 104);

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('amartinez', '2026-06-01 11:01:00', 'LOGIN_FALLIDO', '192.168.5.100', 'Contrasena incorrecta', 104);

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('amartinez', '2026-06-01 11:02:00', 'LOGIN_FALLIDO', '192.168.5.100', 'Bloqueo por multiples intentos fallidos', 104);

INSERT INTO bitacora_seguridad (login_usuario, fecha_evento, accion, ip_origen, detalles, usuario_id)
VALUES ('amartinez', '2026-06-02 09:00:00', 'LOGIN_EXITOSO', '192.168.5.100', 'Inicio de sesion exitoso despues de desbloqueo', 104);
