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


## ------------------------------------------------------------
def menu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    MENU_TEXT = """
      -- MENÚ --
1- Crear táboa artigo   2- Eliminar táboa artigo  3- Engadir artigo
4- Borrar artigo        5- Mostrar artigo         6- Mostrar artigos por prezo
7- Modificar artigo     8- Modificar prezo
q - Saír   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '3':
            insert_row(conn)  
        elif tecla == '4':
            delete_row(conn)  
        elif tecla == '5':
            show_row(conn)  
        elif tecla == '6':
            show_by_price(conn)  
        elif tecla == '7':
            update_row(conn)  
        elif tecla == '8':
            increase_price(conn)  
            
            
## ------------------------------------------------------------
def main():
    """
    Función principal. Conecta á bd e executa o menú.
    Cando sae do menú, desconecta da bd e remata o programa
    """
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)

## ------------------------------------------------------------
if __name__ == '__main__':
    main()