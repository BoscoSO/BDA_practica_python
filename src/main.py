#!/usr/bin/python3
# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.errorcodes
import sys

from datetime import datetime

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
    contraseña_dada = input('Contraseña: ')

    sql = "SELECT id_cliente, contraseña FROM cliente WHERE email = %(e)s"
    idC = -1
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        try:
            cur.execute(sql, {'e': email})
            row = cur.fetchone()
            if row is None:
                print("Usuario no encontrado")
            else:
                contraseña = row['contraseña']       
                if contraseña_dada == contraseña:
                    print("Logeado correctamente")
                    idC= row['id_cliente']            
                else:
                    print("Contraseña incorrecta")  
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()
    return idC

def productoPorPrecio(conn):
    """
    Busca productos dado un precio máximo
    """
    precio_max = input('Precio máximo (por ejemplo 20.15): ')
   
    sql = "SELECT * FROM Producto WHERE precio < %(p)s ORDER BY precio DESC"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p': precio_max})
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")


def valoracionMedia(conn):
    """
    Calcula la valoración media de un producto .
    (no se guarda en la BD, se calcula con AVG(valoracion))
    """
    id_producto = input('ID del producto: ')
    sql = "SELECT AVG(valoracion), COUNT(valoracion) FROM Reseña WHERE id_producto = %(p)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p': id_producto})
            row = cursor.fetchone()
            if row is None:
                print("Producto no encontrado")
            else:
                print(f"Valoración media ({row['count']} valoraciones): {row['avg']}")
        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")

def reseñasProducto(conn):
    """
    Encuentra las reseñas de un producto.
    """
    id_producto = input('ID del producto: ')
    sql = "SELECT * FROM reseña WHERE id_producto = %(p)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p': id_producto})
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")

def reseñasCliente(conn, id_usuario):
    """
    Encuentra las reseñas de un cliente.
    ERROR: si el cliente no está logeado (id_cliente = -1)
    """
    sql = "SELECT * FROM reseña WHERE id_cliente = %(r)s"

    if (id_usuario == -1):
        print("ERROR: Cliente no logeado")
    else:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            try:
                cursor.execute(sql, {'r': id_usuario})
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            except psycopg2.Error as e:
                print(f"Erro {e.pgcode}: {e.pgerror}")


#   CREATE
## ------------------------------------------------------------
def registrarCliente(conn):
    """
    Crea un nuevo cliente con los siguientes datos.
    """
    dni = input('DNI: ')
    if dni=="": dni=None
    nombre = input('Nombre: ')
    if nombre=="": nombre=None
    apellidos = input('Apellidos: ')
    if apellidos=="": apellidos=None
    telefono = input('Teléfono: ')
    if telefono=="": telefono=None
    email = input('Email: ')
    if email=="": email=None
    contraseña = input('Contraseña: ')
    if contraseña=="": contraseña=None
    contraseña_repetida = input('Repetir contraseña: ')
   
    if contraseña_repetida!=contraseña :
        print("Las contraseñas no coinciden")
        return


    sql = "INSERT INTO Cliente (dni, nombre, apellidos ,email ,contraseña ,telefono) VALUES (%(d)s,%(n)s,%(a)s,%(e)s,%(c)s, %(t)s)"
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, {'d': dni, 'n': nombre, 'a': apellidos, 'e': email, 'c': contraseña, 't': telefono})
            conn.commit()
            print("Cliente registrado con éxito.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla cliente.") 
            elif e.pgcode== psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Ya existe una cuenta con ese email o telefono, pruebe con otro")
            elif e.pgcode== psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'dni' in e.pgerror:
                    print("El dni del cliente es necesario.")
                elif 'nombre' in e.pgerror:
                    print("El nombre deel cliente es necesario")
                elif 'apellidos' in e.pgerror:
                    print("Los apellidos del cliente son necesarios")
                elif 'telefono' in e.pgerror:
                    print("El telefono del cliente es necesario")
                elif 'email' in e.pgerror:
                    print("El email del cliente es necesario")
                elif 'contraseña' in e.pgerror:
                    print("La contraseña del cliente es necesaria")
                elif 'telefono' in e.pgerror:
                    print("El telefono del cliente es necesario")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()

def escribirReseña(conn, id_cliente):
    """
    Pide un id del producto a comentar, un título, un comentario y una valoración del producto
    """
    if id_cliente == -1:
        print('Inicia sesion antes de continuar')
    else:
        id_producto = input('ID del producto: ')
        id_p = None if id_producto=="" else int(id_producto)

        titulo = input('Título: ')
        if titulo=="": titulo=None

        comentario = input('Comentario: ')
        if comentario=="": comentario=None

        valoracion = input('Valoración: ')
        val = None if valoracion=="" else int(valoracion)


        sql = "INSERT INTO Reseña (titulo,comentario,fecha,valoracion,id_producto,id_cliente) VALUES (%(t)s,%(c)s,%(f)s,%(v)s,%(p)s, %(u)s)"
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql, {'t': titulo, 'c': comentario, 'f': datetime.now(), 'v': val, 'p': id_p, 'u': id_cliente})
                conn.commit()
                print("Reseña creada con éxito.")
            except psycopg2.Error as e:
                if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                    print("No existe la tabla reseña.") 
                if e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                    print("No existe el producto.") 
                elif e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION:
                    print("La valoracion ha de ser entre 1 y 10")
                elif e.pgcode== psycopg2.errorcodes.NOT_NULL_VIOLATION:
                    if 'id_producto' in e.pgerror:
                        print("El identificador del producto es necesario.")
                    if 'titulo' in e.pgerror:
                        print("El titulo de la reseña es necesario.")
                    if 'comentario' in e.pgerror:
                        print("El comentario de la reseña es necesario.")
                    if 'valoracion' in e.pgerror:
                        print("La valoracion de la reseña es necesaria.")
                else:
                    print(f"Error {e.pgcode}: {e.pgerror}")
                conn.rollback()




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
def fullMenu(conn,id_cliente):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Cambiar contraseña                   2- Buscar productos por precio  
3- Valoración media de un producto      4- Reseñas de un producto
5- Reseñas de un cliente                6- Escribir reseña              
7- Borrar reseña                        8- Cambiar precio de un producto
q- Cerrar sesion

"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            cambiarContraseña(conn)
        elif tecla == '2':
            productoPorPrecio(conn)
        elif tecla == '3':
            valoracionMedia(conn)
        elif tecla == '4':
            reseñasProducto(conn)
        elif tecla == '5':
            reseñasCliente(conn, id_cliente)
        elif tecla == '6':
            escribirReseña(conn, id_cliente)
        elif tecla == '7':
            borrarReseña(conn, id_cliente)
        elif tecla == '8':
            cambiarPrecioProducto(conn)
 
            
            
def simpleMenu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Registrarse                  2- Log in (para mas opciones)
3- Buscar productos por precio  4- Valoración media de un producto  
5- Reseñas de un producto
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
            id_cliente = logIn(conn)
            if id_cliente!=-1 :
                fullMenu(conn,id_cliente)
                id_cliente=-1
        elif tecla == '3':
            productoPorPrecio(conn)
        elif tecla == '4':
            valoracionMedia(conn)
        elif tecla == '5':
            reseñasProducto(conn)
        
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
    simpleMenu(conn)
    disconnect_db(conn)

## ------------------------------------------------------------
if __name__ == '__main__':
    main()