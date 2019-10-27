from lexer import Lexer
from parser import Parser

text_input = """
var x : int;
x := 12 + 6;
var t : int;
t := 15;
if (18 = x){
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
    print('Symbols Table name ' + str(sym) + ' = ' + str(pg.get_names().getSymbol(sym)))
