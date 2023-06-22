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

def registrarUsuario(conn):
    """
    Crea un nuevo usuario con los datos proporcionados.
    :param conn: conexión abierta a la bd
    :return: Nada
    """

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

def alquilar(conn, id_user):
    """
    1. Pide el nombre de la película
    2. Comprueba que no la tenga alquilada
    3. Confirmar importe
    4. Crea una nueva fila de alquiler
    """
    return 1;

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

    sql = "SELECT id, contrasena FROM Usuario WHERE email = %(e)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'e': email})
            row = cursor.fetchone()
            if row is None:
                print("Usuario no encontrado")
            else:
                if contraseña == row['contrasena']:
                    print("Logeado correctamente")
                    userMenu(conn, row['id'])
                else:
                    print("Contraseña incorrecta")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Usuario.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")

def buscarPorNombre(conn):
    """
    1. Pide el nombre de la película
    2. La recupera y muestra título, descripción, duración y precio
    """
    return 1;

def buscarPorCategoria(conn):
    """
    1. Pide el nombre de la categoría
    2. Busca el id de la categoría con ese nombre
    3. Recupera todas las pelis con ese id_categoria y muestra su título y precio
    """
    return 1;

## UPDATE-------------------------------------------------------

def cambiarContraseña(conn, id_user):
    """
    1. Pide la contraseña antigua
    2. Pide la contraseña nueva
    3. Actualiza la contraseña
    """
    return 1;

def hacerDescuento(conn, id_user):
    """
    1. Busca la película
    2. Comprueba que el precio de la peli es estrictamente mayor que 0
    3. Dice el descuento que quiere hacer: 40% p.e.
    4. Crea una fila en descuento INSERT INTO Descuento VALUES (descripcion,descuento,precio_orig,fecha_inicio,fecha_fin)
    5. Actualiza en Pelicula el precio al descuento% del descuento
    """
    return 1;

## DELETE-------------------------------------------------------

def borrarUsuario(conn, id_user):
    """
    1. Pide la contraseña para confirmar el borrado
    2. Borra el Usuario y lo manda al menú simple
    """
    return 1;

def borrarDescuento(conn, id_user):
    """
    1. Pide el título de una película
    2. Busca si tiene descuento y lo coge
    3. Actualiza el precio de la película al precio_original de descuento
    4. Borra el descuento
    """
    return 1;

## MULTIPLES DML---------------------------------------------------

def compartirPelicula(conn, id_user):
    """
    1. Muestra los id y títulos de las películas alquiladas
    2. Se lo puedes mandar a un usuario especificando su correo
    3. Comprueba que el correo exista
    4. Comprueba que no tenga un alquiler con ese correo y fecha límite posterior a hoy
    5. Hace un update de compartida a true
    6. Inserta una nueva fila de alquiler con el id_usuario del email especificado
    """
    return 1;


## MENU--------------------------------------------------------
        
# client menu
def userMenu(conn, id_user):
    """
    Imprime un menú de opciones para un usuario logeado, solicita a opción e executa a función asociada.
    'q' para cerrar sesión y volver al menú base.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Cambiar contraseña               2- Buscar pelicula por nombre 
3- Buscar peliculas por categoria   4- Alquilar una pelicula
5- Borrar cuenta                    6- Compartir pelicula
7- Hacer descuento                  8- Borrar descuento             
q- Cerrar sesion
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == '1':
            cambiarContraseña(conn, id_user)
        if tecla == '2':
            buscarPorNombre(conn)
        if tecla == '3':
            buscarPorCategoria(conn)
        if tecla == '4':
            alquilar(conn, id_user)
        if tecla == '5':
            borrarUsuario(conn, id_user)
        if tecla == '6':
            compartirPelicula(conn, id_user)
        if tecla == '7':
            hacerDescuento(conn, id_user)
        if tecla == '8':
            borrarDescuento(conn, id_user)
        if tecla == 'q':
            break
        
# simple menu
def simpleMenu(conn):
    """
    Imprime un menú de opciones, solicita la opción y executa la función asociada.
    'q' para salir.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Registrarse                  2- Log in (para más opciones)
3- Buscar pelicula por nombre   4- Buscar peliculas por categoria  
q- Salir   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == '1':
            registrarUsuario(conn)
        if tecla == '2':
            logIn(conn)
        if tecla == '3':
            buscarPorNombre(conn)
        if tecla == '4':
            buscarPorCategoria(conn)
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
    
    simpleMenu(conn)

    disconnect_db(conn)

if __name__ == '__main__':
    main()