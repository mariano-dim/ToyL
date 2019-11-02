from toy_x.symbolsWrapper import SymbolsWrapper
from toy_x.utils.pila import Pila


class SymbolTable():
    def __init__(self):
        self.symbols = {}

    def get_all_symbols(self):
        return self.symbols

    def get_symbol(self, symbol):
        heap = self.symbols.get(symbol)
        # Si no existe Pila, la creo
        if heap:
            return heap.desapilar()
        else:
            raise ValueError("set_symbol_value. ID {} no fue declarado".format(symbol))

    def set_symbol_value(self, symbol, value):
        # Value es el valor de un IDentificador. Busco el ID en el diccionario
        # Cuando se elimina el elemento de la pila se debe eliminar tambien del diccionario
        if symbol in self.symbols.keys():
            # La Pila debe existir si o si
            heap = self.symbols[symbol]
            if heap:
                sw = heap.desapilar()
                if sw:
                    # Seteo el valor y vuelvo a apilar el elemento
                    sw.set_value(value)
                    heap.apilar(symbol)
                else:
                    raise ValueError(
                        "set_symbol_value. ID {} no posee su estructura de datos interna con datos".format(symbol))
            else:
                raise ValueError("set_symbol_value. ID {} no posee su estructura de datos interna asociada".format(symbol))
        else:
            raise ValueError("set_symbol_value. ID {} no fue declarado".format(symbol))

    def create_symbol(self, symbol, type):
        # Hay que tener en cuenta si el id es local o no. Una forma de manejar esto es a traves de
        # una pila, es decir, se apila cuando se ingresa a un bloque y se desapila cuando se sale del
        # mismo o se finaliza la operacion
        # Se crean N pilas, una para cada id, lo primero es chequear si existe o no la misma

        heap = self.symbols.get(symbol)
        # Si no existe Pila, la creo
        if heap is None:
            heap = Pila()
            self.symbols[symbol] = heap
        else:
            # Si la Pila existe la obtengo
            heap = self.symbols[symbol]

        sb = SymbolsWrapper(symbol, type)
        heap.apilar(sb)
        print(sb)