from sly import Lexer
import os
import sys
from toyl.ast import BaseASTNode

class ToyLexer(Lexer):
    tokens = {NUMBER_TYPE, STRING_TYPE, OPEN_PARENS, CLOSE_PARENS, COLON,
              INT, STRING, BEGIN, END, PLUS, IF, WHILE, DO, WILDCARD,
              BIGGER, SEMI_COLON, EQUALS, ID, VAR, ELSE, PRINT,
              MINUS, MUL, DIV, DIFF, EQUAL, SMALLER, FOR, TO, DOWNTO}

    # String containing ignored characters (between tokens)
    ignore = ' \t'

    PLUS = r'\+'
    WILDCARD = r'\->'
    MINUS = r'-'
    MUL = r'\*'
    DIV = r'/'
    EQUALS = r':='
    COLON = r'\:'
    BIGGER = r'\>'
    SMALLER = r'\<'
    EQUAL = r'\='
    DIFF = r'\!='
    OPEN_PARENS = r'\('
    CLOSE_PARENS = r'\)'
    SEMI_COLON = r'\;'

    # Numero
    NUMBER_TYPE = r'[0-9][0-9]*'

    # Cadena de texto
    STRING_TYPE = r'"([^"\n]|(\\"))*"'

    # Regla de identificador basico (ID)
    ID = r'[a-zA-Z][a-zA-Z_0-9_]*'
    # Casos especiales
    ID['if'] = IF
    ID['else'] = ELSE
    ID['var'] = VAR
    ID['to'] = TO
    ID['downto'] = DOWNTO
    ID['while'] = WHILE
    ID['for'] = FOR
    ID['do'] = DO
    ID['print'] = PRINT
    ID['int'] = INT
    ID['string'] = STRING
    ID['begin'] = BEGIN
    ID['end'] = END

    ignore_comment = r'\#.*'

    # Define a rule so we can track line numbers
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        columna = self.find_column(self.text, t)
        BaseASTNode.add_result(
            'Error en Lexer; Caracter inesperado. Linea {}, Columna {}, Valor {} '.format(self.lineno, columna,
                                                                                          t.value[0]))
        self.index += 1

        # Compute column.
        #     input is the input text string
        #     token is a token instance

    def find_column(self, text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column


if __name__ == '__main__':
    data = '''begin
 ?   var Y : int;
    Y := 10;asdadsda&

end
    '''
    lexer = ToyLexer()
    for tok in lexer.tokenize(data):
        print(tok)

    # content = ""  # Esta variable mandendra el contenido del archivo de entrada leido
    # path = os.getcwd()
    #
    # print('|-|-|-|-|-|-|-|-|-|-|-|-|-|-  Starting Interpreter  |-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|- \n')
    # print("Leyendo archivo...")
    #
    # # Verifico que el usuario haya ingresado el nombre del archivo como parametro
    # try:
    #     fileName = sys.argv[1]
    # except:
    #     print(
    #         "[ERROR] Se esperaba el nombre de archivo, como parametro para iniciar procesamiento, por ejemplo: 'demo.x'")
    #     exit
    #
    # # Chequeo si la extension del archivo es correcta
    # if fileName[len(fileName) - 2:len(fileName)] != ".x":
    #     print("[ERROR] Extension de archivo no reconocida, asegurese que la extension del archivo sea '.x'")
    #     exit
    #
    # # Abre el archivo de entrada (en modo lectura) y lo graba en la variable 'content'
    # try:
    #     with open(path + "/" + fileName, "r") as sourceCodeFile:
    #         content = sourceCodeFile.read()
    # except:
    #     print('[ERROR] No se puede encontrar el archivo "' + fileName + '"')
    #
    # # Create lexer
    # print("Tokenizando...")
    # lexer = ToyLexer()
    # # print(content)
    #
    # for tok in lexer.tokenize(content):
    #     #print('TOKEN: {token:' '<15} {val:' '>15}'.format(token=tok.type, val=tok.value))
    #     print(tok)
