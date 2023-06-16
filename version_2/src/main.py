#!/usr/bin/python3
# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.errorcodes
import sys

from datetime import datetime

## DB_CONNECTION------------------------------------------------------------
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="pythonbda",
            user="bda",
            password="BDA2223"
        )
        conn.autocommit = False
        return conn
    except psycopg2.Error as e:
        print(f"No se pudo conectar: {e}. Abortando programa")
        sys.exit(1)

def disconnect_db(conn):
    conn.commit()
    conn.close()

##  INSERT-----------------------------------------------------

# Cliente
def registrarCliente(conn):
    """
    Crea un nuevo cliente con los datos proporcionados.
    :param conn: conexión abierta a la bd
    :return: Nada
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
        return -1


    sql = "INSERT INTO Cliente (dni, nombre, apellidos ,email ,contrasena ,telefono, fecha_alta) VALUES (%(d)s,%(n)s,%(a)s,%(e)s,%(c)s,%(t)s,%(f)s)"
    
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, {'d': dni, 'n': nombre, 'a': apellidos, 'e': email, 'c': contraseña, 't': telefono, 'f': datetime.now()})
            conn.commit()
            print("Cliente registrado con éxito.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Cliente.") 
            elif e.pgcode== psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Ya existe una cuenta con ese email o telefono, pruebe con otro")
            elif e.pgcode== psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'email' in e.pgerror:
                    print("El email del cliente es necesario")
                elif 'contraseña' in e.pgerror:
                    print("La contraseña del cliente es necesaria")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()


## SELECT-------------------------------------------------------

# Cliente
def logIn(conn):
    """
    Obtiene la fila con ese email y compara la contraseña de la BD con la proporcionada.
    :param conn: conexión abierta a la bd
    :return: Nada
    """

    email = input('Email: ')
    contraseña = input('Contraseña: ')

    sql = "SELECT id_cliente, contrasena FROM cliente WHERE email = %(e)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'e': email})
            row = cursor.fetchone()
            if row is None:
                print("Usuario no encontrado")
            else:
                if contraseña == row['contrasena']:
                    print("Logeado correctamente")
                    ##fullMenu(conn, row['id_cliente'])
                else:
                    print("Contraseña incorrecta")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Cliente.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")


## UPDATE-------------------------------------------------------

## DELETE-------------------------------------------------------



## MENU--------------------------------------------------------
# admin menu
def adminMenu(conn, id_cliente):
    """
    Imprime un menú de opciones para un usuario logeado, solicita a opción e executa a función asociada.
    'q' para cerrar sesión y volver al menú base.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Añadir pelicula           2- Borrar categoria
3- Crear Categoria           6- Aplicar descuento
q- Cerrar sesion
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        
# client menu
def clientMenu(conn, id_cliente):
    """
    Imprime un menú de opciones para un usuario logeado, solicita a opción e executa a función asociada.
    'q' para cerrar sesión y volver al menú base.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Cambiar contraseña           2- Buscar peliculas por categoria 
3- Alquilar una pelicula        4- Borrar cuenta                      
5- Compartir pelicula           
q- Cerrar sesion
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        
# main menu
def menu(conn):
    """
    Imprime un menú de opciones, solicita la opción y executa la función asociada.
    'q' para salir.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Registrarse                     2- Log in (para mas opciones)
3- Buscar peliculas por categoria  q- Salir   
"""

    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        

## MAIN--------------------------------------------------------
def main():
    """
    Función principal. Se conecta a la bd y ejecuta el menú.
    Cuando sale del menú, se desconecta de la bd y cierra el programa
    """
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    print('Conectado.')
    
    menu(conn)

    disconnect_db(conn)

if __name__ == '__main__':
    main()