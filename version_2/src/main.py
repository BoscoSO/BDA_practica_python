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

# Usuario
def registrarUsuario(conn):
    """
    Crea un nuevo usuario con los datos proporcionados.
    :param conn: conexión abierta a la bd
    :return: Nada

    NIVEL DE AISLAMIENTO:
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    
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


    sql = "INSERT INTO Cliente (nombre, apellidos ,email ,contrasena ,telefono, fecha_alta) VALUES (%(n)s,%(a)s,%(e)s,%(c)s,%(t)s,%(f)s)"
    
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, {'n': nombre, 'a': apellidos, 'e': email, 'c': contraseña, 't': telefono, 'f': datetime.now()})
            conn.commit()
            print("Cliente registrado con éxito.")
        except psycopg2.Error as e:
            if e.pgcode== psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Ya existe una cuenta con ese email o telefono, pruebe con otro")
            elif e.pgcode== psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'nombre' in e.pgerror:
                    print("El nombre del cliente es necesario")
                elif 'apellidos' in e.pgerror:
                    print("Los apellidos del cliente son necesarios")
                elif 'email' in e.pgerror:
                    print("El email del cliente es necesario")
                elif 'contraseña' in e.pgerror:
                    print("La contraseña del cliente es necesaria")
                elif 'telefono' in e.pgerror:
                    print("El telefono del cliente es necesario")
            
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()

# Alquiler
def alquilar(conn, id_user):
    """
    1. Pide el nombre de la película
    2. Comprueba que no la tenga alquilada (que no haya un alquiler de la misma película con un a fecha límite posterior)
    3. Confirmar importe
    4. Crea una nueva fila de alquiler

    NIVEL DE AISLAMIENTO:
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    
    sqlSelect = "SELECT id, precio FROM Pelicula WHERE titulo = %(t)s"
    sqlCheck = "SELECT fecha_limite FROM Alquiler WHERE id_usuario = %(u)s && id_pelicula = %(p)s "
    sqlInsert = "INSERT INTO Alquiler(id_usuario, id_pelicula, fecha_venta, fecha_limite, importe, compartida) VALUES (%(u)s,%(p)s,%(v)s,%(l)s,%(i)s,%(c)s)"
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            titulo = input('Título de película: ')
            cursor.execute(sqlSelect, {'t': titulo})
            row = cursor.fetchone()
            if row is None:
                print("No hay películas con ese nombre")
            else:
                cursor.execute(sqlCheck, {'u': id_user, 'p': row['id']})
                row1= cursor.fetchone()
                if row1['fecha_limite'] > datetime.now():
                    print("Ya tienes un alquiler vigente de la pelicula")
                else:
                    cursor.execute(sqlInsert, {'u': id_user, 'p': row['id'], 'v':  datetime.now(), 'l':  (datetime.now() + datetime.timedelta(days=7)),'i': row['precio'], 'c': False})
                    conn.commit()
                    print("Alquiler realizado con éxito.")
            conn.commit()

        except psycopg2.Error as e:
            if e.pgcode== psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'fecha_venta' in e.pgerror:
                    print("fecha_venta no puede ser nulo")
                elif 'fecha_limite' in e.pgerror:
                    print("fecha_limite no puede ser nulo")
                elif 'importe' in e.pgerror:
                    print("importe no puede ser nulo")
                elif 'compartida' in e.pgerror:
                    print("compartida no puede ser nulo")
            else:                   
                print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()

  

## SELECT-------------------------------------------------------



def logIn(conn):
    """
    Obtiene la fila con ese email y compara la contraseña de la BD con la proporcionada.
    :param conn: conexión abierta a la bd
    :return: Nada

    NIVEL DE AISLAMIENTO:
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)

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
            print(f"Erro {e.pgcode}: {e.pgerror}")



def buscarPorTitulo(conn):
    """
    1. Pide el título de la película
    2. La recupera y muestra título, descripción, duración, precio y director

    NIVEL DE AISLAMIENTO:
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    
    titulo=input("Inserta el título de la película a buscar: ")
    sql = "SELECT titulo, duracion, precio, descripcion, director FROM Pelicula WHERE titulo = %(t)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'t': titulo})
            row = cursor.fetchone()
            if row is None:
                print("No hay películas con ese nombre")
            else:
                print(f"Título: {row['titulo']}")
                print(f"Duración: {row['duracion']}")
                print(f"Precio: {row['precio']}")
                print(f"Director: {row['director']}")
                print(f"Descripcion: {row['descripcion']}")
            conn.commit()

        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()



def buscarPorCategoria(conn):
    """
    1. Imprime los nombres de todas las categorías
    2. Pide el nombre de la categoría
    3. Busca el id de la categoría con ese nombre
    4. Recupera todas las pelis con ese id_categoria y muestra su título, duración y precio

    NIVEL DE AISLAMIENTO:
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)

    sql1 = "SELECT nombre FROM categoria"
    sql2 = "SELECT titulo, duracion, precio FROM Pelicula p JOIN Categoria c ON p.id_categoria = c.id WHERE c.nombre = %(n)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql1)
            categorias = cursor.fetchall()
            if cursor.rowcount == 0:
                print("No hay categorías en este momento :(")
            else:
                print(f"{cursor.rowcount} categorías disponibles:")
                for categoria in categorias:
                    print(f"{categoria['nombre']}")
                
                nombre=input("Inserta el nombre de la categoría a buscar: ")

                cursor.execute(sql2, {'n': nombre})
                peliculas = cursor.fetchall()
                if cursor.rowcount == 0:
                    print("No hay películas dentro de esta categoría :(")
                else:
                    print(f"{cursor.rowcount} películas disponibles:")
                    for pelicula in peliculas:
                        print(f"{pelicula['titulo']}, {pelicula['duracion']}, {pelicula['precio']}")

            conn.commit()

        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()



## UPDATE-------------------------------------------------------



def cambiarContraseña(conn, id_user):
    """
    1. Pide la contraseña antigua
    2. Pide la contraseña nueva
    3. Comprueba que la contraseña antigua es la misma y actualiza la contraseña

    NIVEL DE AISLAMIENTO:
    SERIALIZABLE - Necesitamos saber si la contraseña se ha actualizado o si la cuenta fue borrada.
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

    contraseña_antigua = input("Contraseña antigua: ")
    contraseña_nueva = input("Contraseña nueva: ")

    sql1 = "SELECT contrasena FROM User WHERE id = %(i)s"
    sql2 = "UPDATE User SET contrasena = %(c)s WHERE id = %(i)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql1, {'i': id_user})
            row = cursor.fetchone()
            if contraseña_antigua == row['contrasena']:
                cursor.execute(sql2, {'c': contraseña_nueva}, {'i': id_user})
                print("Contraseña actualizada correctamente")
            else:
                print("Contraseña incorrecta")
            
            conn.commit()

        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("La tabla user no existe. No se puede cambiar la contraseña.")
            if e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION:
                print("La nueva contraseña debe tener al menos 5 caracteres.")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No se pudo cambiar la contraseña porque otra instancia la modificó.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()



def extenderAlquiler(conn, id_user):
    """
    1. Muestra los alquileres con fecha_límite mayor a hoy
    2. Pide el id del alquiler que quiera extender
    3. Actualiza la fecha_límite del alquiler una semana más y suma al importe el precio de la película
    """
    return 1



## DELETE-------------------------------------------------------



def borrarUsuario(conn, id_user):
    """
    1. Pide la contraseña para confirmar el borrado
    2. Borra el Usuario y lo manda al menú simple
    """
    return 1



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
    return 1



## MENU--------------------------------------------------------
        


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
7- Extender alquiler          
q- Cerrar sesion
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == '1':
            cambiarContraseña(conn, id_user)
        if tecla == '2':
            buscarPorTitulo(conn)
        if tecla == '3':
            buscarPorCategoria(conn)
        if tecla == '4':
            alquilar(conn, id_user)
        if tecla == '5':
            borrarUsuario(conn, id_user)
        if tecla == '6':
            compartirPelicula(conn, id_user)
        if tecla == '7':
            extenderAlquiler(conn, id_user)
        if tecla == 'q':
            break
        


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
            buscarPorTitulo(conn)
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
