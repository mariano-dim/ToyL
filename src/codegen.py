from __future__ import print_function
from lexer import Lexer
from parser import Parser

text_input = """
var x;
x := 4 * 4 + 2;
SE (x = 17){
    x := 3;
} SENAO {
    x := x+1;
}
print(x);
"""


# Create lexer
lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)
# Create parser
pg = Parser()
pg.parse()
parser = pg.get_parser()

parser.parse(tokens).eval()


