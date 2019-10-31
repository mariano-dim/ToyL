from toy_x.symbolsWrapper import SymbolsWrapper


class SymbolTable():
    def __init__(self):
        self.symbols = {}

    def get_all_symbols(self):
        return self.symbols

    def get_symbol(self, symbol):
        if symbol in self.symbols.keys():
            value = self.symbols[symbol]
            return value
        else:
            raise ValueError("get_symbol. Variable {} not declared".format(symbol))

    def set_symbol(self, symbol, value):
        if symbol in self.symbols.keys():
            # Value puede ser un numero, una cadena.. o un el resultado de una expresion
            # Si es un identificador esta ok, debo obtener al valor asociado
            self.symbols[symbol].set_value(value)
        else:
            raise ValueError("set_symbol. Variable {} not declared".format(symbol))

    def create_symbol(self, symbol, type):
        # Hay que tener en cuenta si el id es local o no. Una forma de manejar esto es a traves de
        # una pila, es decir, se apila cuando se ingresa a un bloque y se desapila cuando se sale del
        # mismo o se finaliza la operacion
        self.symbols[symbol] = SymbolsWrapper(symbol, type, None)
