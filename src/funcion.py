#!/usr/bin/python3
# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.errorcodes


#Gets varios
#   Ver Reseñas de un usuario
#   Ver Reseña
#   Ver Productos
#   Ver producto
#   Ver cliente
#Post
#   Nuevo Producto
#   Nuevo Cliente
#   Nueva Reseña (actualiza la valoracion del producto)
#Put
#   Cambiar Reseña
#   Cambiar contrasña
#Delete
#   Borrar Reseña


## Nuevo Cliente ------------------------------------------------------------

def insert_row(conn):
    """
    Pide por teclado os datos dun artigo e insértao na táboa
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    scod=input("Código: ")
    cod = None if scod=="" else int(scod)
    nome=input("Nome: ")
    if nome=="": nome=None
    sprezo=input("Prezo: ")
    prezo = None if sprezo=="" else float(sprezo)


    sql = "insert into artigo (codart,nomart,prezoart) values(%(c)s, %(n)s, %(p)s)"
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, {'c': cod, 'n': nome, 'p': prezo})
            conn.commit()
            print("Artigo engadido.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("A táboa artigo non existe. NON se pode engadir o artigo.") 
            elif e.pgcode== psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"O código {cod} xa existe, non se engade o artigo")
            elif e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION:
                print("O prezo debe ser positivo, non se engade o artigo")
            elif e.pgcode== psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("O prezo máximo son 999.99")
            elif e.pgcode== psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if 'codart' in e.pgerror:
                    print("O código do artigo é necesario.")
                else:
                    print("O nome do artigo é necesario")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
def delete_row(conn):
    """
    Pide por teclado os datos dun artigo e bórrao
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    scod=input("Código: ")
    cod = None if scod=="" else int(scod)

    sql = "delete from artigo where codart = %s"

    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, (cod, ) )
            conn.commit()
            if cursor.rowcount == 0:
                print("O artigo non existe.")
            else:
                print("Artigo borrado")
        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
def show_row(conn, control_tx=True):
    """
    Pide por teclado os datos dun artigo e mostra os detalles
    :param conn: a conexión aberta á bd
    :param control_tx: indica se hai que facer commit/rollback ou non
    :return: Nada
    """
    scod=input("Código: ")
    cod = None if scod=="" else int(scod)

    sql = "select nomart, prezoart from artigo where codart = %(c)s"

    retval = None
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'c':cod} )
            row=cursor.fetchone()
            if row is None:
                print("O artigo non existe")
            else:
                prezo = "Descoñecido" if row['prezoart'] is None else row["prezoart"]
                print(f"Cód: {cod}  Nome: {row['nomart']}    Prezo: {prezo}")
                retval = cod
            if control_tx:
                conn.commit()
        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")
            if control_tx:
                conn.rollback()
    return retval

## ------------------------------------------------------------
def show_by_price(conn):
    """
    Pide por teclado un prezo e mostra o detalle dos artigos con prezo maior
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    sprezo=input("Prezo: ")
    prezo = None if sprezo=="" else float(sprezo)

    sql = "select codart, nomart, prezoart from artigo where prezoart > %(p)s"

    # with conn.cursor() as cursor:
    #     try:
    #         cursor.execute(sql, {'p':prezo} )
    #         for (c,n,p) in cursor.fetchall():
    #             print(f"Código: {c}     Nome: {n}      Prezo: {p}")
    #         print(f"Atopados {cursor.rowcount} artigos.")
    #         conn.commit()
    #     except psycopg2.Error as e:
    #         print(f"Erro {e.pgcode}: {e.pgerror}")
    #         conn.rollback()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            cursor.execute(sql, {'p':prezo} )
            rows=cursor.fetchall()
            for row in rows:
                print(f"Código: {row['codart']}     Nome: {row['nomart']}      Prezo: {row['prezoart']}")
            print(f"Atopados {cursor.rowcount} artigos.")
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
def update_row(conn):
    """
    Chama a show_row para pedir un código e mostrar os detalles dun artigo, 
    pide novo nome e prezo, e actualiza o artigo
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    cod = show_row(conn, control_tx=False)
    if cod is None:
        conn.rollback()
        return

    nome=input("Nome: ")
    if nome=="": nome=None
    sprezo=input("Prezo: ")
    prezo = None if sprezo=="" else float(sprezo)


    sql = """
            update artigo
            set nomart = %(n)s,
                    prezoart = %(p)s
            where codart = %(c)s
        """
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, {'c': cod, 'n': nome, 'p': prezo})
            input("Pulsa ENTER")
            conn.commit()
            print("Artigo modificado.")
        except psycopg2.Error as e:
            if e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION:
                print("O prezo debe ser positivo, non se modifica o artigo")
            elif e.pgcode== psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("O prezo máximo son 999.99")
            elif e.pgcode== psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print("O nome do artigo é necesario")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
def increase_price(conn):
    """
    Chama a show_row para pedir un código e mostrar os detalles dun artigo, 
    pide incremento para o prezo, e actualiza o artigo
    :param conn: a conexión aberta á bd
    :return: Nada
    """

    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)

    cod = show_row(conn, control_tx=False)
    if cod is None:
        conn.rollback()
        return

    sincr=input("Incremento de prezo (porcentaxe): ")
    incr = None if sincr=="" else float(sincr)


    sql = """
            update artigo
            set prezoart = prezoart + prezoart * %(i)s / 100
            where codart = %(c)s
        """
    with conn.cursor() as cursor:
        try:
            cursor.execute(sql, {'c': cod, 'i':incr})
            input("Pulsa ENTER para continuar")
            conn.commit()
            print("Prezo modificado.")
        except psycopg2.Error as e:
            if e.pgcode== psycopg2.errorcodes.CHECK_VIOLATION:
                print("O prezo debe ser positivo, non se modifica o artigo")
            elif e.pgcode== psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
                print("O prezo máximo son 999.99")
            elif e.pgcode == psycopg2.errorcodes.SERIALIZATION_FAILURE:
                print("Non se pode modificar o prezo porque outro usuario o modificou.")
            else:
                print(f"Erro {e.pgcode}: {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
