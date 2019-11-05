grammar ToyX;

program
    : BEGIN statement_list END
    | BEGIN empty END
    | empty
    ;

statement_list
    : statement
    | statement_list statement
    ;

statement
    : IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END ELSE BEGIN statement_list END
    | IF OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END
    | WHILE OPEN_PARENS rel CLOSE_PARENS BEGIN statement_list END
    | DO BEGIN statement_list END WHILE OPEN_PARENS rel CLOSE_PARENS
    | FOR ID EQUALS for_list DO BEGIN statement_list END
    | VAR ID COLON INT SEMI_COLON
    | VAR ID COLON STRING SEMI_COLON
    | ID EQUALS expr SEMI_COLON
    | PRINT OPEN_PARENS print_expr_list CLOSE_PARENS SEMI_COLON
    ;

print_expr_list
    : print_expr_list WILDCARD expr
    | WILDCARD expr
    ;

for_list
   : initial_value OPEN_PARENS TO CLOSE_PARENS final_value
   | initial_value OPEN_PARENS DOWNTO CLOSE_PARENS final_value
   ;

initial_value
   : expr
   ;

final_value
   : expr
   ;

rel
    : expr BIGGER expr
    | expr SMALLER expr
    | expr EQUAL expr
    | expr DIFF expr
    ;

expr
    : expr PLUS expr
    | expr MINUS expr
    | expr MUL expr
    | expr DIV expr
    | OPEN_PARENS expr CLOSE_PARENS
    | factor
    | MINUS expr
    ;

factor
    : NUMBER_TYPE
    | STRING_TYPE
    | ID
    ;

empty
    :
    ;

// Keywords
BEGIN:                          'begin';
END:                            'end';
VAR:                            'var';
IF:                             'if';
ELSE:                           'else';
WHILE:                          'while';
DO:                             'do';
PRINT:                          'print';
INT:                            'int';
STRING:                         'string';
TO:                             'to';
FOR:                            'for';
DOWNTO:                         'downto';


OPEN_PARENS:                    '(';
CLOSE_PARENS:                   ')';
SEMI_COLON:                     ';';
COLON:                          ':';
EQUALS:                         ':=';
BIGGER:                         '>';
SMALLER:                        '<';
EQUAL:                          '=';
DIFF:                           '!=';
PLUS:                           '+';
MINUS:                          '-';
MUL:                            '*';
DIV:                            '/';
WILDCARD:                        '->';
COMMA:                          ',';

NUMBER_TYPE
    :  [0-9] [0-9]*
    ;

STRING_TYPE
    :  '\".[a-zA-Z_0-9 _:,.;=]*?"'
    ;

ID
    :   ('a' .. 'z' | 'A' .. 'Z') ('a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_')*
    ;

NEWLINE            : RN                {HandleNewLine();}  -> channel(HIDDEN);
WS                 : [ \t]+            {HandleSpaces();}   -> channel(HIDDEN);
COMMENT            : '#' ~[\r\n\f]*                        -> channel(HIDDEN);

fragment RN
    : '\r'? '\n'
    ;
