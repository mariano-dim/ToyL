from toyl.symbolsWrapper import SymbolsWrapper
from toyl.utils.pila import Pila


class SymbolTable():
    """ Representa una table de simbolos. Internamente la tabla es un diccionario, donde
        el valor de cada key es una pila"""

    def __init__(self):
        self.symbols = {}

    def get_all_symbols(self):
        return self.symbols

    def get_symbol(self, symbol):
        # Una vez que consulto el elemento, debo tener cuidado de no eliminarlo de la pila
        heap = self.symbols.get(symbol)
        # Si no existe Pila, la creo
        if heap:
            value = heap.desapilar()
            heap.apilar(value)
            return value
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
                    heap.apilar(sw)
                else:
                    raise ValueError(
                        "set_symbol_value. ID {} no posee su estructura de datos interna con datos".format(symbol))
            else:
                raise ValueError(
                    "set_symbol_value. ID {} no posee su estructura de datos interna asociada".format(symbol))
        else:
            raise ValueError("set_symbol_value. ID {} no fue declarado".format(symbol))

    def create_symbol(self, symbol, type, location=None):
        # Hay que tener en cuenta si el id es local o no. Una forma de manejar esto es a traves de
        # una pila, es decir, se apila cuando se ingresa a un bloque y se desapila cuando se sale del
        # mismo o se finaliza la operacion.
        # Se crean N pilas, una para cada id, lo primero es chequear si existe o no la misma
        # Debo verificar que para el entorno o scope actual no existe otro identificador con el mismo nombre.

        # Siempre voy a apilar un nuevo elemento o simbolo en la pila
        sb = SymbolsWrapper(symbol, type, None, location)

        heap = self.symbols.get(symbol)
        # Si no existe Pila, la creo
        if heap is None:
            heap = Pila()
            self.symbols[symbol] = heap
        else:
            # Si la Pila existe la obtengo
            heap = self.symbols[symbol]

        heap.apilar(sb)

    def create_local_symbol(self, symbol, local_symbols):
        symbol_index = 0
        try:
            symbol_index = local_symbols.index(symbol)
        except ValueError:
            symbol_index = -1

        if not symbol_index == -1:
            raise ValueError("Habia una Declaracion previa de {} en el scope local".format(symbol))
        else:
            print('Agregando variable {} al scope local'.format(symbol))
            local_symbols.append(symbol)
