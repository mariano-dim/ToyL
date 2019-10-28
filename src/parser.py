from rply import ParserGenerator
from symbolTable import SymbolTable
from ast import (Number, Add, Sub, Mul, Div,
                 If, Statements, Bigger, Smaller,
                 Equal, Different, VarDec,
                 Identifier, IfElse, Print, Assignation)


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names, accepted by the parser.
            ['NUMBER', 'OPEN_PARENS', 'CLOSE_PARENS', 'COLON',
             'INT', 'STRING', 'BEGIN', 'END',
             'PLUS', 'MINUS', 'MUL', 'DIV', 'IF',
             'BIGGER', 'SMALLER', 'EQUAL', 'DIFF',
             'SEMI_COLON',
             'EQUALS', 'ID', 'VAR', 'ELSE', 'PRINT'
             ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ('nonassoc', ['SMALLER', 'BIGGER']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV']),
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

        @self.pg.production('statement_list : statement')
        def statement_list_one(p):
            return Statements(p[0])

        @self.pg.production('statement_list : statement_list statement')
        def statement_list_rest(p):
            p[0].add_child(p[1])
            return p[0]

        @self.pg.production('statement : IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END')
        def statement_if(p):
            return If(p[2], p[5])

        @self.pg.production(
            'statement : IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END ELSE BEGIN statement_list END')
        def statement_if(p):
            return IfElse(p[2], p[5], p[9])

        @self.pg.production('statement : VAR ID COLON INT SEMI_COLON')
        @self.pg.production('statement : VAR ID COLON STRING SEMI_COLON')
        def var_dec(p):
            return VarDec(p[1], p[3], self.symbol_table)

        @self.pg.production('statement : ID EQUALS expr SEMI_COLON')
        def assign(p):
            left = p[0]
            right = p[2]
            return Assignation(left, right, self.symbol_table)

        @self.pg.production('statement : PRINT OPEN_PARENS expr CLOSE_PARENS SEMI_COLON')
        def print_func(p):
            value = p[2]
            return Print(value, self.symbol_table)

        @self.pg.production('rel : expr BIGGER expr')
        @self.pg.production('rel : expr SMALLER expr')
        @self.pg.production('rel : expr EQUAL expr')
        @self.pg.production('rel : expr DIFF expr')
        def rel(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == 'BIGGER':
                return Bigger(left, right, self.symbol_table)
            elif p[1].gettokentype() == 'SMALLER':
                return Smaller(left, right, self.symbol_table)
            elif p[1].gettokentype() == 'EQUAL':
                return Equal(left, right, self.symbol_table)
            elif p[1].gettokentype() == 'DIFF':
                return Different(left, right, self.symbol_table)
            else:
                raise AssertionError('Oops, this should not be possible!')

        @self.pg.production('statement : expr')
        def statement_expr(p):
            return p[0]

        @self.pg.production('expr : term PLUS term')
        @self.pg.production('expr : term MINUS term')
        def expr_binop(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == 'PLUS':
                return Add(left, right, self.symbol_table)
            elif p[1].gettokentype() == 'MINUS':
                return Sub(left, right, self.symbol_table)
            else:
                raise AssertionError('Oops, this should not be possible!')

        @self.pg.production('expr : term')
        def expr_term(p):
            return p[0]

        @self.pg.production('term : factor MUL factor')
        @self.pg.production('term : factor DIV factor')
        def term(p):
            left = p[0]
            right = p[2]
            if p[1].gettokentype() == 'MUL':
                return Mul(left, right, self.symbol_table)
            elif p[1].gettokentype() == 'DIV':
                return Div(left, right, self.symbol_table)
            else:
                raise AssertionError('Oops, this should not be possible!')

        @self.pg.production('term : factor')
        def term_factor(p):
            return p[0]

        @self.pg.production('factor : NUMBER')
        def factor_number(p):
            return Number(p[0])

        @self.pg.production('factor : ID')
        def identifier(p):
            return Identifier(p[0], self.symbol_table)

        @self.pg.production('factor : OPEN_PARENS expr CLOSE_PARENS')
        def expr_parens(p):
            return p[1]

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
