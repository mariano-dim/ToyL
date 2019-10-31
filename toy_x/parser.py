from rply import ParserGenerator
from toy_x.symbolTable import SymbolTable
from toy_x.ast import (Number, Add, Sub, Mul, Div, String, If, While, DoWhile, Statements,
                       Bigger, Smaller, Equal, Different, VarDec, Identifier, IfElse,
                       Print, Assignation, Empty, ForLoop)


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names, accepted by the parser.
            ['NUMBER_TYPE', 'STRING_TYPE', 'OPEN_PARENS', 'CLOSE_PARENS', 'COLON',
             'INT', 'STRING', 'BEGIN', 'END', 'PLUS', 'IF', 'WHILE', 'DO',
             'BIGGER', 'SEMI_COLON', 'EQUALS', 'ID', 'VAR', 'ELSE', 'PRINT',
             'MINUS', 'MUL', 'DIV', 'DIFF', 'EQUAL', 'SMALLER', 'FOR',
             'TO',
             ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV']),
                ("right", ["UMINUS"]),
            ]
        )
        self.symbol_table = SymbolTable()

    def get_names(self):
        return self.symbol_table

    def parse(self):
        @self.pg.production('program : BEGIN statement_list END')
        def program(p):
            # p is a list of the pieces matched by the right hand side of the rule
            return p[1]

        @self.pg.production('program : BEGIN empty END')
        def program_empty(p):
            return Empty()

        @self.pg.production('program : empty')
        def program_empty(p):
            return Empty()

        @self.pg.production('statement_list : statement')
        def statement_list_one(p):
            return Statements(p[0])

        @self.pg.production('statement_list : statement_list statement')
        def statement_list_rest(p):
            p[0].add_child(p[1])
            return p[0]

        @self.pg.production('statement : FOR ID EQUALS expr TO expr DO BEGIN statement_list END')
        def statement_list_rest(p):
            return ForLoop(p[1], p[3], p[5], p[8], self.symbol_table)

        @self.pg.production('statement : IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END')
        def statement_if(p):
            return If(p[2], p[5])

        @self.pg.production(
            'statement : IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END ELSE BEGIN statement_list END')
        def statement_if(p):
            return IfElse(p[2], p[5], p[9])

        @self.pg.production('statement : WHILE OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END')
        def statement_if(p):
            return While(p[2], p[5])

        @self.pg.production('statement : WHILE OPEN_PARENS rel CLOSE_PARENS BEGIN error END')
        def statement_if(p):
            print("Error de sintaxis en statement WHILE. Expresion erronea")

        @self.pg.production('statement : DO BEGIN statement_list END WHILE OPEN_PARENS rel CLOSE_PARENS')
        def statement_if(p):
            return DoWhile(p[6], p[2])

        @self.pg.production('statement : DO BEGIN error END WHILE OPEN_PARENS rel CLOSE_PARENS')
        def statement_if(p):
            print("Error de sintaxis en statement DO-WHILE. Expresion erronea")

        @self.pg.production('statement : VAR ID COLON INT SEMI_COLON')
        @self.pg.production('statement : VAR ID COLON STRING SEMI_COLON')
        def var_dec(p):
            return VarDec(p[1], p[3], self.symbol_table)

        @self.pg.production('statement : ID EQUALS expr SEMI_COLON')
        def assign(p):
            left = p[0]
            right = p[2]
            return Assignation(left, right, self.symbol_table)

        @self.pg.production('statement : ID EQUALS error SEMI_COLON')
        def assign(p):
            print("Error de sintaxis en statement ASSIGN. Expresion erronea")

        @self.pg.production('statement : PRINT OPEN_PARENS expr CLOSE_PARENS SEMI_COLON')
        def print_func(p):
            value = p[2]
            return Print(value, self.symbol_table)

        @self.pg.production('statement : PRINT OPEN_PARENS error CLOSE_PARENS SEMI_COLON')
        def print_func(p):
            print("Error de sintaxis en statement PRINT. Expresion erronea")

        @self.pg.production('rel : expr BIGGER expr')
        @self.pg.production('rel : expr SMALLER expr')
        @self.pg.production('rel : expr EQUAL expr')
        @self.pg.production('rel : expr DIFF expr')
        def rel(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == 'BIGGER':
                return Bigger(left, right, self.symbol_table)
            if p[1].gettokentype() == 'SMALLER':
                return Smaller(left, right, self.symbol_table)
            if p[1].gettokentype() == 'EQUAL':
                return Equal(left, right, self.symbol_table)
            if p[1].gettokentype() == 'DIFF':
                return Different(left, right, self.symbol_table)
            else:
                raise AssertionError('Error, no es posible este valor en una operacion rel!')

        @self.pg.production('expr : expr PLUS expr')
        @self.pg.production('expr : expr MINUS expr')
        @self.pg.production('expr : expr MUL expr')
        @self.pg.production('expr : expr DIV expr')
        def expr_binop(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == 'PLUS':
                return Add(left, right, self.symbol_table)
            if p[1].gettokentype() == 'MINUS':
                return Sub(left, right, self.symbol_table)
            if p[1].gettokentype() == 'MUL':
                return Mul(left, right, self.symbol_table)
            if p[1].gettokentype() == 'DIV':
                return Div(left, right, self.symbol_table)
            else:
                raise AssertionError('Oops, this should not be possible!')

        @self.pg.production('expr : OPEN_PARENS expr CLOSE_PARENS')
        def expr_parens(p):
            return p[1]

        # @self.pg.production("expr : MINUS expr", precedence="UMINUS")
        # def expr_uminus(p):
        #     return -p[1]

        @self.pg.production('expr : factor')
        def term_factor(p):
            return p[0]

        @self.pg.production('factor : NUMBER_TYPE')
        def factor_number_type(p):
            return Number(p[0])

        @self.pg.production('factor : STRING_TYPE')
        def factor_string_type(p):
            return String(p[0])

        @self.pg.production('factor : ID')
        def identifier(p):
            return Identifier(p[0], self.symbol_table)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

        @self.pg.production('empty :')
        def p_empty(p):
            pass

    def get_parser(self):
        return self.pg.build()
