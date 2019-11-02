#!/usr/bin/python
#
#  Proyecto X
#  xinitializer.py
#
#  Creado el 29/09/2019
#  Mariano Andres Di Maggio <mariano.dim@gmail.com>
#

import os
import sys
from builtins import print
from toy_x.lexer import Lexer
from toy_x.parser import Parser
from toy_x.ast import BaseASTNode


def main():
    content = ""  # Esta variable mandendra el contenido del archivo de entrada leido
    path = os.getcwd()

    print('|-|-|-|-|-|-|-|-|-|-|-|-|-|-  Starting Interpreter  |-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|- \n')
    print("Leyendo archivo...")

    # Verifico que el usuario haya ingresado el nombre del archivo como parametro
    try:
        fileName = sys.argv[1]
    except:
        print(
            "[ERROR] Se esperaba el nombre de archivo, como parametro para iniciar procesamiento, por ejemplo: 'demo.x'")
        return

    # Chequeo si la extension del archivo es correcta
    if fileName[len(fileName) - 2:len(fileName)] != ".x":
        print("[ERROR] Extension de archivo no reconocida, asegurese que la extension del archivo sea '.x'")
        return

    # Abre el archivo de entrada (en modo lectura) y lo graba en la variable 'content'
    try:
        with open(path + "/" + fileName, "r") as sourceCodeFile:
            content = sourceCodeFile.read()
    except:
        print('[ERROR] No se puede encontrar el archivo "' + fileName + '"')

    # Create lexer
    lexer = Lexer().get_lexer()
    tokens = lexer.lex(content)

    for tok in tokens:
        print('TOKEN: {token:' '<15} {val:' '>15}'.format(token=tok.gettokentype(),
                                                          val=tok.getstr()))

    # Create lexer again, because vars are in a bad state
    lexer = Lexer().get_lexer()
    tokens = lexer.lex(content)

    # Create parser
    pg = Parser()
    pg.parse()
    parser = pg.get_parser()
    tokens = parser.parse(tokens).eval()

    names = pg.get_names().get_all_symbols()
    print('Imprimiendo tabla de simbolos')
    for sym in names.keys():
        print('Simbolo : ' + str(sym) + ' = ' + str(pg.get_names().get_symbol(sym).get_value()) + ' - '
        + pg.get_names().get_symbol(sym).get_type() )
        #+ ' - ' + pg.get_names().get_symbol(sym).get_location() )

    # Imprimiendo el resultado de la lista de resultados del programa
    for op in BaseASTNode.get_result():
        print(op)



if __name__ == '__main__':
    main()
