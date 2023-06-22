CREATE USER bda WITH PASSWORD 'BDA2223';
ALTER USER bda CREATEDB;

CREATE DATABASE pythonbda OWNER = bda;

\c pythonbda bda;

DROP TABLE Usuario;
DROP TABLE Pelicula;
DROP TABLE Categoria;
DROP TABLE Alquiler;



CREATE TABLE Usuario (
    id          BIGSERIAL       CONSTRAINT UsuarioPK PRIMARY KEY,
    nombre      VARCHAR(64)     NOT NULL,
    apellidos   VARCHAR(64)     NOT NULL,
    email       VARCHAR(128)    UNIQUE NOT NULL,
    contrasena  VARCHAR(128)    NOT NULL,
    telefono    VARCHAR(16)     UNIQUE NOT NULL,
    fecha_alta  DATE            NOT NULL,
    CONSTRAINT LengthContrasena CHECK (LENGTH(contrasena) >= 5)
);

CREATE TABLE Pelicula (
    id              BIGSERIAL       CONSTRAINT PeliculaPK PRIMARY KEY,
    titulo          VARCHAR(128)    UNIQUE NOT NULL,
    descripcion     VARCHAR(1024)   NOT NULL,
    director        VARCHAR(128)    NOT NULL,
    duracion        INT             NOT NULL, 
    precio          FLOAT           NOT NULL,
    id_categoria    BIGINT,
    CONSTRAINT PeliculaCategoriaFK  FOREIGN KEY (id_categoria) REFERENCES Categoria (id) ON DELETE SET NULL,
    CONSTRAINT DuracionPelicula     CHECK (duracion >= 0),
    CONSTRAINT PrecioPelicula       CHECK (precio >= 0)
);
CREATE INDEX PeliculaCategoria ON Pelicula (titulo);
CREATE INDEX PeliculaCategoria ON Pelicula (id_categoria);

CREATE TABLE Categoria (
    id          BIGSERIAL       CONSTRAINT CategoriaPK PRIMARY KEY,
    nombre      VARCHAR(64)     UNIQUE NOT NULL,
    descripcion VARCHAR(1024)
);

CREATE TABLE Alquiler (
    id              BIGSERIAL   CONSTRAINT AlquilerPK PRIMARY KEY,
    id_usuario      BIGINT,
    id_pelicula     BIGINT,
    fecha_venta     DATE         NOT NULL,
    fecha_limite    DATE         NOT NULL,
    importe         FLOAT        NOT NULL,
    compartida      BOOLEAN      NOT NULL,
    CONSTRAINT AlquilerUsuarioFK    FOREIGN KEY (id_usuario) REFERENCES Usuario (id) ON DELETE SET NULL,
    CONSTRAINT AlquilerPeliculaFK   FOREIGN KEY (id_pelicula)   REFERENCES Pelicula (id) ON DELETE SET NULL,
    CONSTRAINT ImporteAlquiler      CHECK (precio_venta >= 0),
    CONSTRAINT FechaLimiteAlquiler  CHECK (fecha_limite > fecha_venta)
);
CREATE INDEX AlquilerUsuario ON Alquiler (id_usuario);



/* INSERCION DE DATOS */

INSERT INTO Categoria(nombre,descripcion) VALUES ("sci-fi","ciencia ficcion");
INSERT INTO Categoria(nombre) VALUES ("comedia");

INSERT INTO Pelicula(titulo, descripcion, director, duracion, precio, id_categoria) VALUES ("peli1", "descripcion1", "director1", 120, 3.99, 0);
INSERT INTO Pelicula(titulo, descripcion, director, duracion, precio, id_categoria) VALUES ("peli2", "descripcion2", "director2", 120, 3.99, 1);
 