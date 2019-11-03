from sly import Lexer


class ToyLexer(Lexer):

    tokens = {NUMBER_TYPE, STRING_TYPE, OPEN_PARENS, CLOSE_PARENS, COLON,
              INT, STRING, BEGIN, END, PLUS, IF, WHILE, DO,
              BIGGER, SEMI_COLON, EQUALS, ID, VAR, ELSE, PRINT,
              MINUS, MUL, DIV, DIFF, EQUAL, SMALLER, FOR, TO, DOWNTO}

    # String containing ignored characters (between tokens)
    ignore = ' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'#.*\n'

    # Base ID rule
    ID = r'[a-zA-Z][a-zA-Z_0-9_]*'

    # Numero (Por ahora un entero muy especial)
    NUMBER_TYPE = r'\d+'

    # Cadena de texto
    STRING_TYPE = r'\".[a-zA-Z_0-9 ]*?\"'

    # Special cases
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


    PLUS = r'\+'
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

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    def startLexer(self):
        print("Inicializando Lexer...")
