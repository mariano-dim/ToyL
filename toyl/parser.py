from sly import Parser
from toyl.lexer import ToyLexer
from toyl.symbolTable import SymbolTable
from toyl.ast import (Number, Add, Sub, Mul, Div, String, If, While, DoWhile, Statements,
                      Bigger, Smaller, Equal, Different, VarDec, Identifier, IfElse, PrintParams,
                      Print, Assignation, Empty, ForLoop, ForList, MinusExpression, GrammarError,
                      )
from toyl.utils.pila import Pila

# El scope se apila y se desapila y es un indicador que se asocia a cada identificador
# Con la unica mision de determinar si la variable esta o no definida en su scope
# Por facilidad lo defino global, asi se ve lo mismo desde cualquier punto
scopes = Pila()
# Apilo el scope arido
scopes.apilar(0)

class ToyParser(Parser):
    tokens = ToyLexer.tokens
    # debugfile = 'parser.out'
    start = 'program'

    # En la medida que se profundiza en la declaracion de la precedencia, los Tokens van adquiriendo
    # mayor precedencia. En este caso PLUS/MINUS tienen menos precedencia que MUL/DIV y este a su vez
    # tiene menor precedencia que UMINUS
    precedence = (
        ('nonassoc', SMALLER, BIGGER),
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
        # print("Luego de crear el scope y habiendolo destruido")
        return p.statement_list

    # @_('')
    # def program(self, p):
    #     return Empty()

    @_('BEGIN empty END')
    def program(self, p):
        return Empty()

    @_('statement')
    def statement_list(self, p):
        return Statements(p.statement, self.symbol_table)

    @_('statement_list statement')
    def statement_list(self, p):
        p.statement_list.add_child(p.statement)
        return p.statement_list

    @_('IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END')
    def statement(self, p):
        return If(p.rel, p.statement_list, self.symbol_table)

    # @_('IF OPEN_PARENS error CLOSE_PARENS BEGIN statement_list END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement IF, en comparador. Expresion erronea", p)
    #     return GrammarError
    #
    # @_('IF OPEN_PARENS rel CLOSE_PARENS BEGIN error END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement IF en bloque de instrucciones. Expresion erronea", p)
    #     return GrammarError

    @_('IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END ELSE BEGIN statement_list END')
    def statement(self, p):
        return IfElse(p.rel, p.statement_list0, p.statement_list1, self.symbol_table)

    # @_('IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END ELSE BEGIN error END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement IF-ELSE en bloque ELSE. Expresion erronea", p)
    #     return GrammarError
    #
    # @_('IF OPEN_PARENS rel CLOSE_PARENS BEGIN error END ELSE BEGIN statement_list END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement IF-ELSE en bloque IF. Expresion erronea", p)
    #     return GrammarError
    #
    # @_('IF OPEN_PARENS error CLOSE_PARENS BEGIN statement_list END ELSE BEGIN statement_list END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement IF-ELSE, en comparador. Expresion erronea", p)
    #     return GrammarError

    @_('WHILE OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END')
    def statement(self, p):
        # While, al igual que los demas elementos AST, son los constituyentes del arbol AST
        return While(p.rel, p.statement_list, self.symbol_table)

    # @_('WHILE OPEN_PARENS rel CLOSE_PARENS BEGIN error END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement WHILE. Expresion erronea", p)
    #     return GrammarError()
    #
    # @_('WHILE OPEN_PARENS error CLOSE_PARENS BEGIN statement_list END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement WHILE. Expresion erronea", p)
    #     return GrammarError()

    @_('DO BEGIN statement_list END WHILE OPEN_PARENS rel CLOSE_PARENS')
    def statement(self, p):
        return DoWhile(p.rel, p.statement_list, self.symbol_table)

    # @_('DO BEGIN error END WHILE OPEN_PARENS rel CLOSE_PARENS')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement DO-WHILE. Expresion erronea", p)
    #     return GrammarError()
    #
    # @_('DO BEGIN statement_list END WHILE OPEN_PARENS error CLOSE_PARENS')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement DO-WHILE. Expresion erronea", p)
    #     return GrammarError()

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
    #     self.print_error("Error de sintaxis en statement ASSIGN. Expresion erronea", p)
    #     return GrammarError()

    @_('PRINT OPEN_PARENS print_expr_list CLOSE_PARENS SEMI_COLON')
    def statement(self, p):
        return Print(p.print_expr_list, self.symbol_table)

    # @_('PRINT OPEN_PARENS error CLOSE_PARENS SEMI_COLON')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement PRINT. Expresion erronea ", p)
    #     return GrammarError()

    @_('WILDCARD expr')
    def print_expr_list(self, p):
        return PrintParams(p.expr, self.symbol_table)

    @_('print_expr_list WILDCARD expr')
    def print_expr_list(self, p):
        p.print_expr_list.add_child(p.expr)
        return p.print_expr_list

    @_('FOR ID EQUALS for_list DO BEGIN statement_list END')
    def statement(self, p):
        return ForLoop(p.ID, p.for_list, p.statement_list, self.symbol_table)

    # @_('FOR ID EQUALS error DO BEGIN statement_list END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement FOR, en rangos. Expresion erronea", p)
    #     return GrammarError()
    #
    # @_('FOR ID EQUALS for_list DO BEGIN error END')
    # def statement(self, p):
    #     self.print_error("Error de sintaxis en statement FOR, en lista de comandos. Expresion erronea", p)
    #     return GrammarError()

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
        return GrammarError()

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
        return Identifier(p.ID, self.symbol_table)

    @_('')
    def empty(self, p):
        return Empty()

    def print_error(self, baseerror, p):
        print(baseerror
              + ' index ' + str(p.error.index) + ' '
              + ' lineno ' + str(p.error.lineno) + ' '
              + ' type ' + p.error.type + ' '
              + ' value ' + p.error.value)

