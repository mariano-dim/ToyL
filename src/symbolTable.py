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
            self.symbols[symbol] = value
        else:
            raise ValueError("set_symbol. Variable {} not declared".format(symbol))

    def create_symbol(self, symbol, type):
        self.symbols[symbol] = [type, None]
