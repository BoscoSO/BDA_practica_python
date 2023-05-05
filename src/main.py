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
def logIn(conn):
    """
    Busca la fila con ese email y compara la contraseña de la BD con la dada
    """
    email = input('Email: ')
    contraseña = input('Contraseña: ')

def productoPorPrecio(conn):
    """
    Busca productos dado un precio máximo
    """
    precio_max = input('Precio máximo (por ejemplo 20.15): ')

def valoracionMedia(conn):
    """
    Calcula la valoración media de un producto .
    (no se guarda en la BD, se calcula con AVG(valoracion))
    """
    id_producto = input('ID del producto: ')

def reseñasProducto(conn):
    """
    Encuentra las reseñas de un producto.
    """
    id_producto = input('ID del producto: ')

def reseñasCliente(conn, id_usuario):
    """
    Encuentra las reseñas de un cliente.
    ERROR: si el cliente no está logeado (id_cliente = -1)
    """



#   CREATE
## ------------------------------------------------------------
def registrarCliente(conn):
    """
    Crea un nuevo cliente con esos datos.
    """
    dni = input('DNI: ')
    nombre = input('Nombre: ')
    apellidos = input('Apellidos: ')
    teléfono = input('Teléfono: ')
    email = input('Email: ')
    contraseña = input('Contraseña: ')
    contraseña_repetida = input('Repetir contraseña: ')

def escribirReseña(conn, id_cliente):
    """
    Pide un título, un comentario y una valoración del producto
    """
    id_producto = input('ID del producto: ')
    título = input('Título: ')
    comentario = input('Comentario: ')
    valoracion = input('Valoración: ')



#   UPDATE
## ------------------------------------------------------------
def cambiarContraseña(conn):
    """
    Cambia la contraseña de un cliente.
    """
    email = input('Email: ')
    contraseña = input('Contraseña: ')
    contraseña_nueva = input('Nueva contraseña: ')

def cambiarPrecioProducto(conn):
    """
    Cambia el precio de un producto existente.
    """
    id_producto = input('ID del producto: ')
    precio_nuevo = input('Nuevo precio: ')



#   DELETE
## ------------------------------------------------------------
def borrarReseña(conn, id_cliente):
    """
    Borra una reseña que haya escrito el cliente.
    """
    id_reseña = input('ID de la reseña: ')





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
    id_cliente = -1
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            registrarCliente(conn)
        elif tecla == '2':
            cambiarContraseña(conn)
        elif tecla == '3':
            id_cliente = logIn(conn)
        elif tecla == '4':
            productoPorPrecio(conn)
        elif tecla == '5':
            valoracionMedia(conn)
        elif tecla == '6':
            reseñasProducto(conn)
        elif tecla == '7':
            reseñasCliente(conn, id_cliente)
        elif tecla == '8':
            escribirReseña(conn, id_cliente)
        elif tecla == '9':
            borrarReseña(conn, id_cliente)
        elif tecla == '0':
            cambiarPrecioProducto(conn)
            
            
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