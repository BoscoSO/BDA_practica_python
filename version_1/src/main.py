#!/usr/bin/python3
# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.errorcodes
import sys

from datetime import datetime

## ------------------------------------------------------------
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

## ------------------------------------------------------------
def disconnect_db(conn):
    conn.commit()
    conn.close()


#   SELECT por id
## ------------------------------------------------------------
def getProducto(conn):
    """
    Busca un producto por su id.
    :param conn: conexión abierta a la bd
    :return: Nada
    """

    id_producto = input('Id del producto: ')
    if not id_producto.isdigit():
        print("No es un id valido")
        return

    sql = "SELECT * FROM Producto WHERE id_producto = %(p)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p':id_producto})
            row=cursor.fetchone()
            if row == None :
                print("No existe el producto.")
            else:
                return row
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Producto.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")

#   SELECT
## ------------------------------------------------------------
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
                    fullMenu(conn, row['id_cliente'])
                else:
                    print("Contraseña incorrecta")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Cliente.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")


def productoPorPrecio(conn):
    """
    Busca productos por debajo de un precio máximo.
    :param conn: conexión abierta a la bd
    :return: Nada
    """

    precio_max = input('Precio máximo (por ejemplo 20.15): ')
    if not precio_max.replace(".","").isdigit():
        print("No es un numero")
        return

    sql = "SELECT * FROM Producto WHERE precio < %(p)s ORDER BY precio DESC"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p': precio_max})
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Producto.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")


def valoracionMedia(conn):
    """
    Calcula la valoración media de un producto .
    (no se guarda en la BD, se calcula con AVG(valoracion))
    :param conn: conexión abierta a la bd
    :return: Nada
    """
    rowP=getProducto(conn)
    if rowP is None: 
        return
    id_producto=rowP['id_producto']

    sql = "SELECT AVG(valoracion), COUNT(valoracion) FROM Resena WHERE id_producto = %(p)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p': id_producto})
            row = cursor.fetchone()
            if row is None:
                print("Producto no encontrado")
            else:
                if row['count'] == 0:
                    print("No hay reseñas para este producto")
                else:
                    print(f"Valoración media ({row['count']} valoraciones): {row['avg']}")
        except TypeError:
            print("No existe el producto.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Reseña.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")


def reseñasProducto(conn):
    """
    Encuentra las reseñas de un producto.
    :param conn: conexión abierta a la bd
    :return: Nada
    """

    rowP=getProducto(conn)
    if rowP is None: 
        return
    id_producto=rowP['id_producto']

    sql = "SELECT * FROM resena WHERE id_producto = %(p)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p': id_producto})
            rows = cursor.fetchall()
            if len(rows) == 0:
                print("Este producto no tiene reseñas")
                return
            print("Estas son las reseñas del producto: ")
            for row in rows:
                print(row)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Reseña.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")


def reseñasCliente(conn, id_cliente):
    """
    Encuentra las reseñas de un cliente.
    :param conn: conexión abierta a la bd
    :param id_cliente: id del cliente
    :return: Nada
    """

    sql = "SELECT * FROM resena WHERE id_cliente = %(r)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'r': id_cliente})
            rows = cursor.fetchall()
            print("Estas son tus reseñas: ")
            for row in rows:
                print(row)
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Cliente.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")
        





#   CREATE
## ------------------------------------------------------------
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


def subirProducto(conn, id_cliente):
    """
    Sube un nuevo producto a la BD.
    :param conn: conexión abierta a la bd
    :param id_cliente: id del cliente
    :return: Nada
    """

    nombre = input('Nombre: ')
    if nombre=="": nombre=None
    descripcion = input('Descripción: ')
    if descripcion=="": descripcion=None
    fabricante = input('Fabricante: ')
    if fabricante=="": fabricante=None
    precio = input('Precio: ')
    if precio=="": precio=None
    
    if not precio.replace(".","").isdigit():
        print("No es un valor correcto para el precio")
        return

    sql = "INSERT INTO Producto (nombre,descripcion,fabricante,precio,fecha_modificacion,id_cliente) VALUES (%(n)s,%(d)s,%(f)s,%(p)s,%(fm)s,%(c)s)"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'n': nombre, 'd': descripcion, 'f': fabricante, 'p': precio,'fm': datetime.now(), 'c': id_cliente})
            conn.commit()
            print("Producto creado con éxito.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Producto.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'nombre' in e.pgerror:
                    print("El nombre del producto es necesario")
                if 'precio' in e.pgerror:
                    print("El precio del producto es necesario")
            elif e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION:
                print("El precio debe ser mayor a 0")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print("No existe el cliente.")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()


def escribirReseña(conn, id_cliente):
    """
    Pide un id del producto a comentar, un título, un comentario y una valoración del producto
    :param conn: conexión abierta a la bd
    :param id_cliente: id del cliente
    :return: Nada
    """

    rowP=getProducto(conn)
    if rowP is None: 
        return
    id_producto=rowP['id_producto']
    id_p = None if id_producto=="" else int(id_producto)
    titulo = input('Título: ')
    if titulo=="": titulo=None
    comentario = input('Comentario: ')
    if comentario=="": comentario=None
    valoracion = input('Valoración: ')
    if not valoracion.isdigit(): 
        print("la valoración debe ser un entero entre 1 y 10")
        return
    val = None if valoracion=="" else int(valoracion)

    sql = "INSERT INTO Resena (titulo,comentario,fecha,valoracion,id_producto,id_cliente) VALUES (%(t)s,%(c)s,%(f)s,%(v)s,%(p)s, %(u)s)"
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'t': titulo, 'c': comentario, 'f': datetime.now(), 'v': val, 'p': id_p, 'u': id_cliente})
            conn.commit()
            print("Reseña creada con éxito.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Reseña.") 
            if e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print("No existe el producto.") 
            elif e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION:
                print("La valoracion ha de ser entre 1 y 10")
            elif e.pgcode== psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'id_producto' in e.pgerror:
                    print("El identificador del producto es necesario.")
                if 'valoracion' in e.pgerror:
                    print("La valoracion de la reseña es necesaria.")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()




#   UPDATE
## ------------------------------------------------------------
def cambiarContraseña(conn, id_cliente):
    """
    Cambia la contraseña de un cliente.
    :param conn: conexión abierta a la bd
    :param id_cliente: id del cliente
    :return: Nada
    """

    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED)

    email = input('Email: ')
    contraseña = input('Contraseña: ')
    contraseña_nueva = input('Nueva contraseña: ')

    sql = "SELECT id_cliente, contrasena FROM Cliente WHERE email = %(e)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'e': email})
            row = cursor.fetchone()
            if id_cliente == row['id_cliente']:
                if contraseña == row['contrasena']:
                    cursor.execute("UPDATE Cliente SET contrasena = %(n)s WHERE email = %(e)s", {'n': contraseña_nueva, 'e': email})
                    conn.commit()
                    print("Contraseña cambiada con éxito.")
                else:
                    print("Contraseña incorrecta.")
            else:
                print("Solo puedes cambiar la contraseña de esta propia cuenta.")

        except TypeError:
                print("No existe ningun usuario con ese email.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Cliente.")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No se puede modificar la contraseña en estos momentos.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()
                

def cambiarProducto(conn, id_cliente):
    """
    Cambia la información de un producto existente, borrando todas sus reseñas.
    :param conn: conexión abierta a la bd
    :param id_cliente: id del cliente
    :return: Nada
    """

    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED)

    id_producto = input('ID del producto: ')
    nombre = input('Nombre: ')
    if nombre=="": nombre=None
    descripcion = input('Descripcion: ')
    fabricante = input('Fabricante: ')
    precio = input('Precio: ')
    if precio=="": precio=None
    if not precio.replace(".","").isdigit():
        print("No es un valor correcto para el precio")
        return

    sql = "SELECT id_cliente FROM Producto WHERE id_producto = %(p)s"
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p': id_producto})
            row = cursor.fetchone()
            if id_cliente == row['id_cliente']:
                cursor.execute("""UPDATE Producto SET 
                               nombre = %(n)s, 
                               descripcion = %(d)s, 
                               fabricante = %(f)s, 
                               precio = %(p)s,
                               fecha_modificacion = %(fm)s 
                               WHERE id_producto = %(id)s""", {'n': nombre, 'd': descripcion, 'f': fabricante, 'p': precio, 'fm':datetime.now(), 'id': id_producto})
                
                cursor.execute("""DELETE FROM Resena WHERE id_producto = %(id)s""", {'id': id_producto})
                conn.commit()
                print("Producto cambiado con éxito.")
            else:
                print("Ese producto no te pertenece, no puedes modificarlo.")
        except TypeError:
                print("No existe el producto.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Producto.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'nombre' in e.pgerror:
                    print("El nombre del producto es necesario")
                if 'precio' in e.pgerror:
                    print("El precio del producto es necesario")
            elif e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION:
                print("El precio debe ser mayor a 0")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No se puede modificar el producto en estos momentos porque está siendo modificado.")
            else:
                print(f"Error {e.pgcode}: {e.pgerror}")
            conn.rollback()


def cambiarPrecioProducto(conn, id_cliente):
    """
    Cambia el precio de un producto existente.
    :param conn: conexión abierta a la bd
    :param id_cliente: id del cliente
    :return: Nada
    """

    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED);

    rowP=getProducto(conn)
    if rowP is None: 
        return
    id_producto=rowP['id_producto']
    
    descuento = input('Indica la cantidad del descuento (por ejemplo para indicar que es del 20%: 20): ')

    sql = "SELECT id_cliente, precio FROM Producto WHERE id_producto = %(p)s"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p': id_producto})
            row = cursor.fetchone()
            if id_cliente == row['id_cliente']:
                precio_nuevo = row['precio'] * (1-float(descuento)/100)
                cursor.execute("UPDATE Producto SET precio = %(n)s WHERE id_producto = %(p)s", {'n': precio_nuevo, 'p': id_producto})
                conn.commit()
                print(f"Precio cambiado con éxito a [{precio_nuevo}]")
            else:
                print("Ese producto no te pertenece, no puedes cambiar su precio.")
        except TypeError:
                print("No existe el producto.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Producto.")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No se puede cambiar el precio del producto en estos momentos porque está siendo modificado.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()





#   DELETE
## ------------------------------------------------------------
def borrarReseña(conn, id_cliente):
    """
    Borra una reseña que haya escrito el cliente.
    :param conn: conexión abierta a la bd
    :param id_cliente: id del cliente
    :return: Nada
    """

    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

    reseñasCliente(conn, id_cliente)
    id_resena = input('Escribe el ID de la reseña que quieras borrar: ')
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute("SELECT id_cliente FROM Resena WHERE id_resena = %(id)s", {'id': id_resena})
            row = cursor.fetchone()
            if id_cliente == row['id_cliente']:
                cursor.execute("DELETE FROM Resena WHERE id_resena = %(id)s", {'id': id_resena})
                conn.commit()
                print("Reseña borrada con éxito.")
            else:
                print("Esa reseña no te pertenece, no puedes borrarla.")
        except TypeError:
                print("No existe esa reseña.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("No existe la tabla Reseña.")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("No se puede borrar la reseña porque ya ha sido borrada.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()





## ------------------------------------------------------------
def fullMenu(conn, id_cliente):
    """
    Imprime un menú de opciones para un usuario logeado, solicita a opción e executa a función asociada.
    'q' para cerrar sesión y volver al menú base.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Cambiar contraseña                   2- Buscar productos por precio  
3- Valoración media de un producto      4- Reseñas de un producto
5- Reseñas de un cliente                6- Escribir reseña              
7- Borrar reseña                        8- Subir producto
9- Modificar un producto                0- Cambiar precio de un producto
i- Buscar producto por ID               q- Cerrar sesion
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == 'i':
            getProducto(conn)
        elif tecla == '1':
            cambiarContraseña(conn, id_cliente)
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
            subirProducto(conn, id_cliente)
        elif tecla == '9':
            cambiarProducto(conn, id_cliente)
        elif tecla == '0':
            cambiarPrecioProducto(conn, id_cliente)
 
            
            
def simpleMenu(conn):
    """
    Imprime un menú de opciones, solicita la opción y executa la función asociada.
    'q' para salir.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Registrarse                  2- Log in (para mas opciones)
3- Buscar productos por precio  4- Valoración media de un producto  
5- Reseñas de un producto       i- Buscar producto por ID
q- Salir   
"""

    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == 'i':
            getProducto(conn)
        elif tecla == '1':
            registrarCliente(conn)
        elif tecla == '2':
            logIn(conn)
        elif tecla == '3':
            productoPorPrecio(conn)
        elif tecla == '4':
            valoracionMedia(conn)
        elif tecla == '5':
            reseñasProducto(conn)
        
## ------------------------------------------------------------
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

## ------------------------------------------------------------
if __name__ == '__main__':
    main()