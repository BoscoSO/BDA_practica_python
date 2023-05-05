#!/usr/bin/python3
# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.errorcodes
import sys

from funcion import delete_row, increase_price, insert_row, show_by_price, show_row, update_row

## ------------------------------------------------------------
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="bdaPractica",
            user="postgres",
            password="abc123."
        )
        conn.autocommit = False
        return conn
    except psycopg2.Error as e:
        print(f"No se pudo conectar: {e}. Abortando programa")
        sys.exit(1)

## ------------------------------------------------------------
def disconnect_db(conn):
    conn.commit()
    conn.close()





#   SELECT por id
## ------------------------------------------------------------
def getProducto(conn, id_producto):
    """
    Busca un producto por su id.
    """
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM producto WHERE id_producto = %s", (id_producto,))
    return cur.fetchone()

def getCliente(conn, id_cliente):
    """
    Busca un cliente por su id.
    """
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM cliente WHERE id_cliente = %s", (id_cliente,))
    return cur.fetchone()

def getReseña(conn, id_reseña):
    """
    Busca una reseña por su id.
    """
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM reseña WHERE id_reseña = %s", (id_reseña,))
    return cur.fetchone()



#   SELECT
## ------------------------------------------------------------
def logIn(conn, email, contraseña):
    """
    Busca la fila con ese email y compara la contraseña de la BD con la dada
    """

def productoPorPrecio(conn, precio_max):
    """
    Busca productos dado un precio máximo
    """

def valoracionMedia(conn, id_producto):
    """
    Calcula la valoración media de un producto .
    (no se guarda en la BD, se calcula con AVG(valoracion))
    """

def reseñasProducto(conn, id_producto):
    """
    Encuentra las reseñas de un producto.
    """

def reseñasCliente(conn, id_usuario):
    """
    Encuentra las reseñas de un cliente.
    """



#   CREATE
## ------------------------------------------------------------
def registrarCliente(conn, dni, nombre, apellidos, teléfono, email, contraseña, contraseña_repetida):
    """
    Crea un nuevo cliente con esos datos.
    """

def escribirReseña(conn, id_producto, título, comentario, valoracion):
    """
    Pide un título, un comentario y una valoración del producto
    """



#   UPDATE
## ------------------------------------------------------------
def cambiarContraseña(conn, email, contraseña, contraseña_nueva):
    """
    Cambia la contraseña de un cliente.
    """

def cambiarPrecioProducto(conn, id_producto, precio_nuevo):
    """
    Cambia el precio de un producto existente.
    """



#   DELETE
## ------------------------------------------------------------
def borrarReseña(conn, id_reseña):
    """
    Borra una reseña.
    """





## ------------------------------------------------------------
def menu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Registrarse                  2- Cambiar contraseña               3- Log in
4- Buscar productos por precio  5- Valoración media de un producto  6- Reseñas de un producto
7- Reseñas de un cliente        8- Escribir reseña                  9- Borrar reseña
0- Cambiar precio de un producto
q - Salir   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            registrarCliente(conn, dni, nombre, apellidos, teléfono, email, contraseña, contraseña_repetida)
        elif tecla == '2':
            cambiarContraseña(conn, email, contraseña, contraseña_nueva)
        elif tecla == '3':
            logIn(conn, email, contraseña)
        elif tecla == '4':
            productoPorPrecio(conn, precio_max)
        elif tecla == '5':
            valoracionMedia(conn, id_producto)
        elif tecla == '6':
            reseñasProducto(conn, id_producto)
        elif tecla == '7':
            reseñasCliente(conn, id_usuario)
        elif tecla == '8':
            escribirReseña(conn, id_producto, título, comentario, valoracion)
        elif tecla == '9':
            borrarReseña(conn, id_reseña)
        elif tecla == '0':
            cambiarPrecioProducto(conn, id_producto, precio_nuevo)
            
            
## ------------------------------------------------------------
def main():
    """
    Función principal. Conecta á bd e executa o menú.
    Cando sae do menú, desconecta da bd e remata o programa
    """
    # Crear con script_tablas.sql
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)

## ------------------------------------------------------------
if __name__ == '__main__':
    main()