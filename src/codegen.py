from lexer import Lexer
from parser import Parser

text_input = """
var x;
x := 4 * 4 + 2;
var t;
t := 15;
if (16+1 != 18){
    x := 3;
} else {
    x := 1 + 19;
    if (1 +20 =  40-19){
        x := 5;
    }
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
names = pg.get_names().getAllSymbols()
for sym in names.keys():
    print('Symbols Table name  : ' + str(sym))
    print('Symbols Table value : ' + str(pg.get_names().getSymbol(sym)))
