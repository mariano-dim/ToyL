
class SymbolTable():
    def __init__(self):
        self.symbols = {}

    def getAllSymbols(self):
        return self.symbols

    def getSymbol(self, symbol):
        if symbol in self.symbols.keys():
            value = self.symbols[symbol]
            return value
        else:
            raise ValueError("getSymbol. Variable {} not declared".format(symbol))

    def setSymbol(self, symbol, value):
        if symbol in self.symbols.keys():
            # Value puede ser un numero, una cadena.. o un el resultado de una expresion
            # Si es un identificador esta ok, debo obtener al valor asociado
            self.symbols[symbol] = value
        else:
            raise ValueError("setSymbol. Variable {} not declared".format(symbol))

    def createSymbol(self, symbol, type):
        self.symbols[symbol.value] = [type, None]
