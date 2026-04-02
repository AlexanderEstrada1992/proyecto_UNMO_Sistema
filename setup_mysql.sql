-- SCRIPT DE CREACIÓN DE BASE DE DATOS Y TABLAS (PARA MYSQL WORKBENCH O PHPMYADMIN)

-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS unmo_db;
USE unmo_db;

-- 2. Crear tabla de Equipos (Migrada de SQLite)
CREATE TABLE IF NOT EXISTS equipos (
    id_equipo VARCHAR(50) PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    estado_operativo VARCHAR(50) NOT NULL,
    disponibilidad VARCHAR(50) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- 3. Crear tabla obligatoria de Usuarios (Según Rúbrica)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    mail VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- 4. Inserción de un usuario de prueba (Opcional)
INSERT IGNORE INTO usuarios (nombre, mail, password) VALUES ('Administrador UNMO', 'admin@unmo.gob.ec', '123456');

-- 5. Crear tabla de Asignaciones para relacionar equipos con usuarios
CREATE TABLE IF NOT EXISTS asignaciones (
    id_asignacion INT AUTO_INCREMENT PRIMARY KEY,
    id_equipo VARCHAR(50) NOT NULL,
    id_usuario INT NOT NULL,
    fecha_asignacion DATE NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);
