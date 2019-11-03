from sly import Parser
from toy_x.lexer import ToyLexer
from toy_x.symbolTable import SymbolTable
from toy_x.ast import (Number, Add, Sub, Mul, Div, String, If, While, DoWhile, Statements,
                       Bigger, Smaller, Equal, Different, VarDec, Identifier, IfElse,
                       Print, Assignation, Empty, ForLoop, ForList, MinusExpression
                       )


class ToyParser(Parser):
    tokens = ToyLexer.tokens
    # debugfile = 'parser.out'
    start = 'program'

    precedence = (
        ('left', PLUS, MINUS),
        ('left', MUL, DIV),
        ("right", UMINUS),
    )

    def __init__(self):
        self.symbol_table = SymbolTable()

    def get_names(self):
        return self.symbol_table

    @_('BEGIN statement_list END')
    def program(self, p):
        # p is a list of the pieces matched by the right hand side of the rule
        return p.statement_list

    @_('BEGIN empty END')
    def program(self, p):
        return Empty()

    @_('statement')
    def statement_list(self, p):
        return Statements(p.statement)

    @_('statement_list statement')
    def statement_list(self, p):
        p.statement_list.add_child(p.statement)
        return p.statement_list

    @_('IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END')
    def statement(self, p):
        return If(p.rel, p.statement_list)

    @_('IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END ELSE BEGIN statement_list END')
    def statement(self, p):
        return IfElse(p[2], p[5], p[9])

    @_('WHILE OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END')
    def statement(self, p):
        return While(p.rel, p.statement_list)

    # @_('WHILE OPEN_PARENS rel CLOSE_PARENS BEGIN error END')
    # def statement(self, p):
    #     print("Error de sintaxis en statement WHILE. Expresion erronea")

    @_('DO BEGIN statement_list END WHILE OPEN_PARENS rel CLOSE_PARENS')
    def statement(self, p):
        return DoWhile(p.rel, p.statement_list)

    # @_('DO BEGIN error END WHILE OPEN_PARENS rel CLOSE_PARENS')
    # def statement(self, p):
    #     print("Error de sintaxis en statement DO-WHILE. Expresion erronea")

    @_('VAR ID COLON INT SEMI_COLON')
    def statement(self, p):
        return VarDec(p.ID, p.INT, self.symbol_table)

    @_('VAR ID COLON STRING SEMI_COLON')
    def statement(self, p):
        return VarDec(p.ID, p.STRING, self.symbol_table)

    @_('ID EQUALS expr SEMI_COLON')
    def statement(self, p):
        return Assignation(p.ID, p.expr, self.symbol_table)

    # @_('ID EQUALS error SEMI_COLON')
    # def statement(self, p):
    #     print("Error de sintaxis en statement ASSIGN. Expresion erronea")

    @_('PRINT OPEN_PARENS expr CLOSE_PARENS SEMI_COLON')
    def statement(self, p):
        return Print(p.expr, self.symbol_table)

    # @_('PRINT OPEN_PARENS error CLOSE_PARENS SEMI_COLON')
    # def statement(self, p):
    #     print("Error de sintaxis en statement PRINT. Expresion erronea")

    @_('FOR ID EQUALS for_list DO BEGIN statement_list END')
    def statement(self, p):
        return ForLoop(p.ID, p.for_list, p.statement_list, self.symbol_table)

    @_('initial_value OPEN_PARENS TO CLOSE_PARENS final_value')
    def for_list(self, p):
        return ForList(p.initial_value, p.TO, p.final_value)

    @_('initial_value OPEN_PARENS DOWNTO CLOSE_PARENS final_value')
    def for_list(self, p):
        return ForList(p.initial_value, p.DOWNTO, p.final_value)

    @_('expr')
    def initial_value(self, p):
        return p.expr

    @_('expr')
    def final_value(self, p):
        return p.expr

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return MinusExpression(p.expr, self.symbol_table)

    @_('expr BIGGER expr')
    def rel(self, p):
        return Bigger(p.expr0, p.expr1, self.symbol_table)

    @_('expr SMALLER expr')
    def rel(self, p):
        return Smaller(p.expr0, p.expr1, self.symbol_table)

    @_('expr EQUAL expr')
    def rel(self, p):
        return Equal(p.expr0, p.expr1, self.symbol_table)

    @_('expr DIFF expr')
    def rel(self, p):
        return Different(p.expr0, p.expr1, self.symbol_table)

    @_('expr PLUS expr')
    def expr(self, p):
        return Add(p.expr0, p.expr1, self.symbol_table)

    @_('expr MINUS expr')
    def expr(self, p):
        return Sub(p.expr0, p.expr1, self.symbol_table)

    @_('expr MUL expr')
    def expr(self, p):
        return Mul(p.expr0, p.expr1, self.symbol_table)

    @_('expr DIV expr')
    def expr(self, p):
        return Div(p.expr0, p.expr1, self.symbol_table)

    @_('OPEN_PARENS expr CLOSE_PARENS')
    def expr(self, p):
        return p.expr

    @_('factor')
    def expr(self, p):
        return p.factor

    @_('NUMBER_TYPE')
    def factor(self, p):
        return Number(p.NUMBER_TYPE)

    @_('STRING_TYPE')
    def factor(self, p):
        return String(p.STRING_TYPE)

    @_('ID')
    def factor(self, p):
        idr = Identifier(p.ID, self.symbol_table)
        return idr

    # @_('error')
    # def factor(self, p):
    #     print("Syntax error in factor. Bad expression")

    @_('')
    def empty(self, p):
        return Empty()
