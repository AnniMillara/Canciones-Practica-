DROP DATABASE IF EXISTS esquema_canciones;
CREATE DATABASE IF NOT EXISTS esquema_canciones
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE esquema_canciones;

-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario  INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(45)  UNIQUE NOT NULL,
    email       VARCHAR(50)  UNIQUE NOT NULL,
    contrasena  VARCHAR(45)  NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla canciones
CREATE TABLE IF NOT EXISTS canciones (
    id_cancion  INT AUTO_INCREMENT PRIMARY KEY,
    titulo      VARCHAR(100) NOT NULL,
    artista     VARCHAR(50)  NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla favoritos (N:M)
CREATE TABLE IF NOT EXISTS favoritos (
    usuario_id  INT NOT NULL,
    cancion_id  INT NOT NULL,
    PRIMARY KEY (usuario_id, cancion_id),
    CONSTRAINT fk_usuario_cancion
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_cancion_usuario
        FOREIGN KEY (cancion_id) REFERENCES canciones(id_cancion)
        ON DELETE CASCADE ON UPDATE CASCADE
);