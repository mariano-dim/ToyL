from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add('NUMBER', r'\d+')
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
        self.lexer.add('QUOTE', r'\"')
        # Vars
        self.lexer.add('EQUALS', r':=')
        self.lexer.add('COLON', r'\:')
        self.lexer.add('VAR', r'var')
        # Else
        self.lexer.add('ELSE', r'else')
        # If
        self.lexer.add('IF', r'if')
        # Print
        self.lexer.add('PRINT', r'print')
        # Types
        self.lexer.add('INT', r'int')
        self.lexer.add('STRING', r'string')
        # Identifier
        self.lexer.add('ID', r'[a-zA-Z_][a-zA-Z_0-9]*')
        self.lexer.ignore(r'\s+')

        self.lexer.ignore(r'#.*\n')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
