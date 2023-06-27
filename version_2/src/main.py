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
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
    """
    #conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    
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


    sql = "INSERT INTO Usuario(nombre, apellidos ,email ,contrasena ,telefono, fecha_alta) VALUES (%(n)s,%(a)s,%(e)s,%(c)s,%(t)s,NOW())"
    
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, {'n': nombre, 'a': apellidos, 'e': email, 'c': contraseña, 't': telefono})
            conn.commit()
            print("Cliente registrado con éxito.")

        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Ya existe una cuenta con ese email o telefono, pruebe con otro")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                if 'contrasena' in e.pgerror:
                    print(f"La contraseña debe contener mas de 5 caracteres")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'nombre' in e.pgerror:
                    print("El nombre del usuario es necesario")
                elif 'apellidos' in e.pgerror:
                    print("Los apellidos del usuario son necesarios")
                elif 'email' in e.pgerror:
                    print("El email del usuario es necesario")
                elif 'contrasena' in e.pgerror:
                    print("La contraseña del usuario es necesaria")
                elif 'telefono' in e.pgerror:
                    print("El telefono del usuario es necesario")
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
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
    
    titulo = input('Título de película: ')
    if titulo=="": titulo=None
    
    sqlSelect = "SELECT id, precio FROM Pelicula WHERE titulo = %(t)s"
    sqlCheck = "SELECT id FROM Alquiler WHERE id_usuario = %(u)s AND id_pelicula = %(p)s AND fecha_limite > NOW()"
    sqlInsert = "INSERT INTO Alquiler(id_usuario, id_pelicula, fecha_venta, fecha_limite, importe, compartida) VALUES (%(u)s,%(p)s,NOW(),NOW()+ INTERVAL '7 days',%(i)s,%(c)s)"
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sqlSelect, {'t': titulo})
            row = cursor.fetchone()
            if row is None:
                print("No hay películas con ese nombre")
            else:
                cursor.execute(sqlCheck, {'u': id_user, 'p': row['id']})
                row1 = cursor.fetchone()
                if row1 is None:
                    cursor.execute(sqlInsert, {'u': id_user, 'p': row['id'],'i': row['precio'], 'c': False})
                    print("Alquiler realizado con éxito.")
                else:
                    print("Ya tienes un alquiler vigente de la pelicula.")
            
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
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                if 'importe' in e.pgerror:
                    print("El importe del alquiler no puede ser negativo")
                elif 'fecha_limite' in e.pgerror:
                    print("La fecha limite no puede ser anterior a la fecha de venta")
            else:                   
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()

  

## SELECT-------------------------------------------------------



def logIn(conn):
    """
    Obtiene la fila con ese email y compara la contraseña de la BD con la proporcionada.
    :param conn: conexión abierta a la bd
    :return: Nada

    NIVEL DE AISLAMIENTO:
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
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
                    conn.commit()
                    print("Logeado correctamente")
                    return row['id']
                else:
                    conn.commit()
                    print("Contraseña incorrecta")
            
        except psycopg2.Error as e:
            print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()
    return -1


def buscarPorTitulo(conn):
    """
    1. Pide el título de la película
    2. La recupera y muestra título, descripción, duración, precio y director

    NIVEL DE AISLAMIENTO:
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
    
    titulo = input("Inserta el título de la película a buscar: ")
    sql = "SELECT titulo, duracion, precio, director, descripcion FROM Pelicula WHERE titulo = %(t)s"

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
            print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()



def buscarPorCategoria(conn):
    """
    1. Imprime los nombres de todas las categorías
    2. Pide el nombre de la categoría
    3. Busca el id de la categoría con ese nombre
    4. Recupera todas las pelis con ese id_categoria y muestra su título, duración y precio

    NIVEL DE AISLAMIENTO:
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
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
            
                nombre = input("Inserta el nombre de la categoría a buscar: ")

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
            print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()

 

## UPDATE-------------------------------------------------------



def cambiarContraseña(conn, id_user):
    """
    1. Pide la contraseña antigua
    2. Pide la contraseña nueva
    3. Comprueba que la contraseña antigua es la misma y actualiza la contraseña

    NIVEL DE AISLAMIENTO:
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

    contraseña_antigua = input("Contraseña antigua: ")
    contraseña_nueva = input("Contraseña nueva: ")

    sql1 = "SELECT contrasena FROM Usuario WHERE id = %(i)s"
    sql2 = "UPDATE Usuario SET contrasena = %(c)s WHERE id = %(i)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql1, {'i': id_user})
            row = cursor.fetchone()
            if row is None:
                print("No existe este usuario.")
            else:
                if contraseña_antigua == row['contrasena']:
                    cursor.execute(sql2, {'c': contraseña_nueva, 'i': id_user})
                    print("Contraseña cambiada con éxito.")
                else:
                    print("Contraseña incorrecta.")

            conn.commit()

        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No puedes cambiar la contraseña en estos momentos, prueba mas tarde.")
            if e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("La contraseña debe tener 5 o más caracteres.")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()
    
    

def extenderAlquiler(conn, id_user):
    """
    1. Muestra los alquileres con fecha_límite mayor a hoy
    2. Pide el id del alquiler que quiera extender
    3. Actualiza la fecha_límite del alquiler una semana más y suma al importe el precio de la película

    NIVEL DE AISLAMIENTO:
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

    sql1 = "SELECT a.id, titulo, importe, fecha_limite, p.precio FROM Alquiler a JOIN Pelicula p ON a.id_pelicula = p.id WHERE id_usuario = %(i)s AND fecha_limite > NOW()"    
    sql2 = "SELECT a.importe, p.precio FROM Alquiler a JOIN Pelicula p ON a.id_pelicula = p.id WHERE a.id = %(i)s "
    sql3 = "UPDATE Alquiler SET fecha_limite = fecha_limite + INTERVAL '7 days', importe = importe + %(p)s WHERE id = %(i)s"
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql1, {'i': id_user})
            alquileres = cursor.fetchall()
            
            if cursor.rowcount == 0:
                print("En estos momentos no tienes ninguna pelicula alquilada")
            else:
                print(f"{cursor.rowcount} Alquileres disponibles:")
                for alquiler in alquileres:
                    if alquiler['importe'] == 0:
                        print(f"ID {alquiler['id']}: {alquiler['titulo']}, {alquiler['importe']}€, hasta el {alquiler['fecha_limite']}. No ampliable")
                    else:            
                        print(f"ID {alquiler['id']}: {alquiler['titulo']}, {alquiler['importe']}€, hasta el {alquiler['fecha_limite']}. Ampliar una semana [{alquiler['precio']}€]")
                
                id_alquiler = input("Introduce el id del alquiler a extender: ")
                if not id_alquiler.isdigit():
                    print("No es un id valido")
                    return
               
                cursor.execute(sql2, {'i': id_alquiler})
                alquiler = cursor.fetchone()
                
                if alquiler is None:
                    print("No existe un alquiler con ese id.")        
                else:
                    if alquiler['importe'] == 0:
                        print("Este alquiler te lo han compartido, no puedes extenderlo.")
                    else:
                        cursor.execute(sql3, {'p': alquiler['precio'],'i': id_alquiler})
                        print("Alquiler extendido con éxito.")
            
            conn.commit()
                
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                if 'importe' in e.pgerror:
                    print("El importe del alquiler no puede ser negativo")
                elif 'fecha_limite' in e.pgerror:
                    print("La fecha limite no puede ser anterior a la fecha de venta")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No puedes ampliar el alquiler en estos momentos, prueba mas tarde.")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()
                




## DELETE-------------------------------------------------------



def borrarUsuario(conn, id_user):
    """
    1. Pide la contraseña para confirmar el borrado
    2. Borra el Usuario y lo manda al menú simple
    
    NIVEL DE AISLAMIENTO:
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
    """
    #conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

    contraseña = input("Para confirmar la acción introduzca su contraseña: ")

    sql1 = "SELECT contrasena FROM Usuario WHERE id = %(i)s"
    sql2 = "DELETE FROM Usuario WHERE id = %(i)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql1, {'i': id_user})
            row = cursor.fetchone()
            if row is None:
                print("No existe este usuario.")
            else:
                if contraseña == row['contrasena']:
                    cursor.execute(sql2, {'i': id_user})
                    conn.commit()
                    print("Usuario borrado con éxito.")
                    return True;
                else:
                    conn.commit()
                    print("Contraseña incorrecta.")
                                
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Usuario. No se pudo realizar el borrado.")
            #if e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
            #    print("No se puede borrar la cuenta en estos momentos, prueba mas tarde.")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()
    
    return False;



## MULTIPLES DML---------------------------------------------------



def compartirPelicula(conn, id_user):
    """
    1. Muestra los id y títulos de las películas alquiladas
    2. Se lo puedes mandar a un usuario especificando su correo
    3. Comprueba que el correo exista
    4. Comprueba que no tenga un alquiler de esa película y fecha límite posterior a hoy
    5. Hace un update de compartida a true
    6. Inserta una nueva fila de alquiler con el id_usuario del email especificado

    NIVEL DE AISLAMIENTO:
    READ_COMMITTED -
    REPEATABLE_READ -
    SERIALIZABLE -
    """
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
  
    sql1 = "SELECT a.id, titulo, importe, fecha_limite, p.precio FROM Alquiler a JOIN Pelicula p ON a.id_pelicula = p.id WHERE id_usuario = %(i)s AND fecha_limite > NOW()"
    sql2 = "SELECT id FROM Usuario WHERE email = %(e)s"
    sql3 = "SELECT id_pelicula, fecha_limite FROM Alquiler WHERE id = %(i)s"
    sql4 = "SELECT id FROM Alquiler WHERE id_usuario = %(i)s AND id_pelicula = %(p)s AND fecha_limite > NOW()"    
    sql5 = "INSERT INTO Alquiler(id_usuario, id_pelicula, fecha_venta, fecha_limite, importe, compartida) VALUES (%(u)s,%(p)s,NOW(),%(l)s,0,true)"
    sql6 = "UPDATE Alquiler SET compartida = true  WHERE id = %(i)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql1, {'i': id_user})

            alquileres = cursor.fetchall()
            
            if cursor.rowcount == 0:
                print("En estos momentos no tienes ninguna pelicula alquilada")
            else:
                print(f"{cursor.rowcount} Alquileres disponibles:")
                for alquiler in alquileres:
                    print(f"ID {alquiler['id']}: {alquiler['titulo']}, {alquiler['importe']}€, hasta el {alquiler['fecha_limite']}")
                
                id_alquiler = input("Introduce el id del alquiler que quieres compartir: ")
                email_usuario = input("Introduce el email del usuario a quien se lo vas a compartir: ")
          
                cursor.execute(sql2, {'e': email_usuario})
                user = cursor.fetchone()
                if user is None:
                    print("Usuario no encontrado")
                else:
                    cursor.execute(sql3, {'i': id_alquiler})
                    alquiler = cursor.fetchone()
                    if alquiler is None:
                        print("No existe alquiler con ese id")
                    else:
                        if user['id'] == id_user:
                            print("No puedes compartirtela a ti mismo")
                        else:
                            cursor.execute(sql4, {'i': user['id'], 'p': alquiler['id_pelicula']})
                            repetido = cursor.fetchone()
                            if repetido is None:
                                cursor.execute(sql5, {'u': user['id'],'p': alquiler['id_pelicula'],'l': alquiler['fecha_limite']})

                                cursor.execute(sql6, {'i': id_alquiler})
                                print("Alquiler compartido con éxito.")
                            else:
                                print("El usuario ya tiene esa pelicula actualmente alquilada")

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
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                if 'importe' in e.pgerror:
                    print("El importe del alquiler no puede ser negativo")
                elif 'fecha_limite' in e.pgerror:
                    print("La fecha limite no puede ser anterior a la fecha de venta")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No puedes compartir el alquiler en estos momentos, prueba mas tarde.")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()
                

    



## MENU--------------------------------------------------------
        


def userMenu(conn, id_user):
    """
    Imprime un menú de opciones para un usuario logueado, solicita a opción e executa a función asociada.
    'q' para cerrar sesión y volver al menú base.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Cambiar contraseña               2- Buscar pelicula por nombre 
3- Buscar peliculas por categoria   4- Alquilar una pelicula
5- Borrar cuenta                    6- Compartir pelicula
7- Ampliar alquiler          
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
            if borrarUsuario(conn, id_user):
                break
        if tecla == '6':
            compartirPelicula(conn, id_user)
        if tecla == '7':
            extenderAlquiler(conn,id_user)
        if tecla == 'q':
            break
        


def simpleMenu(conn):
    """
    Imprime un menú de opciones para un usuario no logueado, solicita la opción y executa la función asociada.
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
            id_user = logIn(conn)
            if id_user != -1:
                userMenu(conn, id_user)
        if tecla == '3':
            buscarPorTitulo(conn)
        if tecla == '4':
            buscarPorCategoria(conn)
        if tecla == 'q':
            exit()
        


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