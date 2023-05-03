CREATE USER practica WITH PASSWORD 'abc123.' CREATEDB;
CREATE DATABASE bdaPractica WITH OWNER=practica;


CREATE TABLE Cliente (
    id BIGSERIAL PRIMARY KEY,
    dni VARCHAR(9) UNIQUE  NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    apellidos VARCHAR(60) NOT NULL,
    contraseña VARCHAR(60) NOT NULL,
    telefono VARCHAR(60) NOT NULL,
    idioma VARCHAR(60)
);

CREATE INDEX ClienteIndexByNombre ON Cliente (nombre);

CREATE TABLE Producto (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(60) unique NOT NULL,
    descripcion VARCHAR(1024), 
    ingredientes VARCHAR(60) NOT NULL,
    fabricante VARCHAR(60) NOT NULL, 
    cantidadxunidad FLOAT NOT NULL,
    unidad VARCHAR(60) NOT NULL,
    infonutricional VARCHAR(1024) NOT null,
    valoracionMedia FLOAT
);
 
CREATE INDEX ProductoIndexByNombre ON Producto (nombre);


CREATE TABLE Reseña (
    id BIGSERIAL PRIMARY KEY,
	id_producto BIGINT references Producto(id) ON DELETE RESTRICT,
	id_cliente BIGINT references Cliente(id) ON DELETE CASCADE,
    titulo VARCHAR(60)  NOT NULL,
    comentario VARCHAR(1024) NOT NULL,
    fecha SMALLINT NOT NULL,
    valoracion SMALLINT NOT null,
    PRIMARY KEY (id, id_producto, id_cliente)
    
);

CREATE INDEX ReseñaIndexByFecha ON Reseña (fecha);


