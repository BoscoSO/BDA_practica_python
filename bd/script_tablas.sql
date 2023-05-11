CREATE USER BDA WITH PASSWORD 'BDA2223' CREATEDB;
CREATE DATABASE pythonBDA WITH OWNER = BDA;

DROP TABLE Reseña;
DROP TABLE Producto;
DROP TABLE Cliente;



CREATE TABLE Cliente (
    id_cliente BIGSERIAL CONSTRAINT ClientePK PRIMARY KEY,
    dni VARCHAR(9),
    nombre VARCHAR(64),
    apellidos VARCHAR(64),
    email VARCHAR(128) UNIQUE NOT NULL,
    contraseña VARCHAR(128) NOT NULL,
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
 


CREATE TABLE Reseña (
    id_reseña BIGSERIAL CONSTRAINT ReseñaPK PRIMARY KEY,
    titulo VARCHAR(64),
    comentario VARCHAR(1024),
    valoracion SMALLINT NOT NULL,
    fecha DATE,
    id_producto BIGINT NOT NULL,
	id_cliente BIGINT NOT NULL,
    CONSTRAINT ReseñaProductoFK FOREIGN KEY (id_producto) REFERENCES Producto (id_producto) ON DELETE CASCADE,
    CONSTRAINT ReseñaClienteFK FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente) ON DELETE CASCADE,
    CONSTRAINT ValoracionRange CHECK (valoracion > 0 AND valoracion <= 10)
);

CREATE INDEX ReseñaIndexByProducto ON Reseña (id_producto);
CREATE INDEX ReseñaIndexByCliente ON Reseña (id_cliente);