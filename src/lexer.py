from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Operators
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        self.lexer.add('BEGIN', r'begin')
        self.lexer.add('END', r'end')
        # Comp
        self.lexer.add('BIGGER', r'\>')
        self.lexer.add('SMALLER', r'\<')
        self.lexer.add('EQUAL', r'\=')
        self.lexer.add('DIFF', r'\!=')
        self.lexer.add('OPEN_PARENS', r'\(')
        self.lexer.add('CLOSE_PARENS', r'\)')
        self.lexer.add('SEMI_COLON', r'\;')
        # Vars
        self.lexer.add('EQUALS', r':=')
        self.lexer.add('COLON', r'\:')
        self.lexer.add('VAR', r'var')
        # Else
        self.lexer.add('ELSE', r'else')
        # If
        self.lexer.add('IF', r'if')
        # While
        self.lexer.add('WHILE', r'while')
        # Do
        self.lexer.add('DO', r'do')
        # Print
        self.lexer.add('PRINT', r'print')
        # Types
        self.lexer.add('INT', r'int')
        self.lexer.add('STRING', r'string')
        # Numero (Por ahora un entero muy especial)
        self.lexer.add('NUMBER_TYPE', r'\d+')
        # Cadena de texto
        self.lexer.add('STRING_TYPE', r'\".[a-zA-Z_0-9]*?\"')
        # Identifier
        self.lexer.add('ID', r'[a-zA-Z][a-zA-Z_0-9_]*')
        self.lexer.ignore(r'\s+')

        self.lexer.ignore(r'#.*\n')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()


