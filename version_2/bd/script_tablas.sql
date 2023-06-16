CREATE USER bda WITH PASSWORD 'BDA2223';
ALTER USER bda CREATEDB;

CREATE DATABASE pythonbda OWNER = bda;

\c pythonbda bda;


DROP TABLE Categoria;
DROP TABLE Cliente;
DROP TABLE Pelicula;
DROP TABLE Alquiler;


CREATE TABLE Categoria (
    tipo        VARCHAR(16)   CONSTRAINT CategoriaPK PRIMARY KEY,
    descripcion VARCHAR(1024) NOT NULL
);


CREATE TABLE Cliente (
    email       VARCHAR(128) CONSTRAINT ClientePK PRIMARY KEY,
    dni         VARCHAR(9)   UNIQUE NOT NULL,
    nombre      VARCHAR(64)  NOT NULL,
    apellidos   VARCHAR(64)  NOT NULL,
    contrasena  VARCHAR(64)  NOT NULL,
    telefono    VARCHAR(16)  UNIQUE NOT NULL,
    fecha_alta  DATE         NOT NULL
);


CREATE TABLE Pelicula (
    id_pelicula     BIGSERIAL       CONSTRAINT PeliculaPK PRIMARY KEY,
    titulo          VARCHAR(128)    NOT NULL,
    director        VARCHAR(128)    NOT NULL,
    descripcion     VARCHAR(1024)   NOT NULL, 
    duracion        INT             NOT NULL, 
    precio          FLOAT           NOT NULL,
    tipo_categoria  VARCHAR(16),
    CONSTRAINT PeliculaCategoria       FOREIGN KEY (tipo_categoria) REFERENCES Categoria (tipo) ON DELETE SET NULL,
    CONSTRAINT PrecioPeliculaPositivo  CHECK (precio > 0)
);
 
CREATE TABLE Alquiler (
    id_pelicula     VARCHAR(128) NOT NULL,
    email_cliente   VARCHAR(128) NOT NULL,
    fecha_venta     DATE         NOT NULL,
    fecha_limite    DATE         NOT NULL,
    precio_venta    FLOAT        NOT NULL,
    compartible     BOOLEAN      NOT NULL,   
    CONSTRAINT AlquilerPK               PRIMARY KEY (id_pelicula,email_cliente,fecha_venta)
    CONSTRAINT AlquilerPelicula         FOREIGN KEY (id_pelicula)   REFERENCES Pelicula (id_pelicula) ON DELETE CASCADE,
    CONSTRAINT AlquilerCliente          FOREIGN KEY (email_cliente) REFERENCES Cliente (email)        ON DELETE CASCADE,
    CONSTRAINT PrecioAlquilerPositivo   CHECK (precio_venta > 0)
    CONSTRAINT FechaLimiteCorrecta      CHECK (fecha_limite > fecha_venta)
);
 