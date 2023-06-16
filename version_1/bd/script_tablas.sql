CREATE USER bda WITH PASSWORD 'BDA2223';
ALTER USER bda CREATEDB;

CREATE DATABASE pythonbda OWNER = bda;

\c pythonbda bda;


DROP TABLE Resena;
DROP TABLE Producto;
DROP TABLE Cliente;



CREATE TABLE Cliente (
    id_cliente BIGSERIAL CONSTRAINT ClientePK PRIMARY KEY,
    dni VARCHAR(9),
    nombre VARCHAR(64),
    apellidos VARCHAR(64),
    email VARCHAR(128) UNIQUE NOT NULL,
    contrasena VARCHAR(128) NOT NULL,
    telefono VARCHAR(16) UNIQUE,
    fecha_alta DATE
);




CREATE TABLE Producto (
    id_producto BIGSERIAL CONSTRAINT ProductoPK PRIMARY KEY,
    nombre VARCHAR(128) NOT NULL,
    descripcion VARCHAR(1024), 
    fabricante VARCHAR(128), 
    precio FLOAT NOT NULL,
    fecha_modificacion DATE,
    id_cliente BIGINT NOT NULL,
    CONSTRAINT ProductoCliente FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente) ON DELETE CASCADE,
    CONSTRAINT PrecioPositivo CHECK (precio > 0)
);
 


CREATE TABLE Resena (
    id_resena BIGSERIAL CONSTRAINT ResenaPK PRIMARY KEY,
    titulo VARCHAR(64),
    comentario VARCHAR(1024),
    valoracion SMALLINT NOT NULL,
    fecha DATE,
    id_producto BIGINT NOT NULL,
	id_cliente BIGINT NOT NULL,
    CONSTRAINT ResenaProductoFK FOREIGN KEY (id_producto) REFERENCES Producto (id_producto) ON DELETE CASCADE,
    CONSTRAINT ResenaClienteFK FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente) ON DELETE CASCADE,
    CONSTRAINT ValoracionRange CHECK (valoracion > 0 AND valoracion <= 10)
);

CREATE INDEX ResenaIndexByProducto ON Resena (id_producto);
CREATE INDEX ResenaIndexByCliente ON Resena (id_cliente);