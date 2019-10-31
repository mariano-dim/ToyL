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
    | FOR ID EQUALS expr TO expr DO BEGIN statement_list END
    | DO BEGIN statement_list END WHILE OPEN_PARENS rel CLOSE_PARENS
    | VAR ID COLON INT SEMI_COLON
    | VAR ID COLON STRING SEMI_COLON
    | ID EQUALS expr SEMI_COLON
    | PRINT OPEN_PARENS expr CLOSE_PARENS SEMI_COLON
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

NUMBER_TYPE
    :  [1-9] [0-9]*
    ;

STRING_TYPE
    :   '"' ('a' .. 'z' | 'A' .. 'Z') ('a' .. 'z' | 'A' .. 'Z' | '0' .. '9' | '_')* '"'
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
