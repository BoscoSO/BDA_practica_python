CREATE USER practica WITH PASSWORD 'abc123.' CREATEDB;
CREATE DATABASE bdaPractica WITH OWNER=practica;

DROP TABLE Reseña;
DROP TABLE Cliente;
DROP TABLE Producto;


CREATE TABLE Producto (
    id_producto BIGSERIAL CONSTRAINT ProductoPK PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion VARCHAR(1024), 
    fabricante VARCHAR(128) NOT NULL, 
    precio FLOAT NOT NULL,
    CONSTRAINT PrecioPositivo CHECK (precio > 0),
    CONSTRAINT NombreFabricanteUnique UNIQUE (nombre,fabricante)
);
 


CREATE TABLE Cliente (
    id_cliente BIGSERIAL CONSTRAINT ClientePK PRIMARY KEY,
    dni VARCHAR(9) NOT NULL,
    nombre VARCHAR(64) NOT NULL,
    apellidos VARCHAR(64) NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,
    contraseña VARCHAR(128) NOT NULL,
    telefono VARCHAR(16) UNIQUE NOT NULL
);



CREATE TABLE Reseña (
    id_reseña BIGSERIAL CONSTRAINT ReseñaPK PRIMARY KEY,
    titulo VARCHAR(64) NOT NULL,
    comentario VARCHAR(1024),
    fecha DATE NOT NULL,
    valoracion SMALLINT NOT NULL,
    id_producto BIGINT NOT NULL,
	id_cliente BIGINT NOT NULL,
    CONSTRAINT ReseñaProductoFK(id_producto) REFERENCES Producto(id_producto) ON DELETE CASCADE,
    CONSTRAINT ReseñaClienteFK(id_cliente) REFERENCES Cliente(id_cliente) ON DELETE CASCADE,
    CONSTRAINT ValoracionRange CHECK (valoracion > 0 AND valoracion <= 10)
);

CREATE INDEX ReseñaIndexByProducto ON Reseña (id_producto);
CREATE INDEX ReseñaIndexByCliente ON Reseña (id_cliente);