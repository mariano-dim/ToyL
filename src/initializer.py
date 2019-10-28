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
#import xinterpreter

from lexer import Lexer
from parser import Parser


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
    # Create parser
    pg = Parser()
    pg.parse()
    parser = pg.get_parser()
    parser.parse(tokens).eval()
    names = pg.get_names().get_all_symbols()
    for sym in names.keys():
        print('Symbols Table name ' + str(sym) + ' = ' + str(pg.get_names().get_symbol(sym)))




if __name__ == '__main__':
    main()
