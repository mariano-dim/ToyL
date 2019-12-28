from toyl.ast import BaseASTNode
from toyl.symbolsWrapper import SymbolsWrapper
from toyl.utils.pila import Pila


class SymbolTable():
    """ Representa una table de simbolos. Internamente la tabla es un diccionario, donde
        el valor de cada key es una pila"""

    def __init__(self):
        self.symbols = {}

    def get_all_symbols(self):
        return self.symbols

    def remove_scope_variables(self, scope):
        # Si los hay, elimino todos los objetos del scope actual

        # print('Imprimiendo todas las variables del la tabla de simbolos')
        # for sym in self.symbols.keys():
        #     print('Variable : ' + str(sym)
        #           + ' = ' + str(self.get_symbol(sym).get_value())
        #           + ' - ' + self.get_symbol(sym).get_type()
        #           + ' - ' + self.get_symbol(sym).get_location()
        #           + ' - ' + str(self.get_symbol(sym).get_scope()))

        #print('Eliminado elementos para el scope objetivo:' + str(scope))
        # Itero a traves del diccionario mediante una lista. Esto me permite editar la estructura mientras la recorro
        for sym in list(self.symbols):
            # Desapilo elementos de cada una de las Pilas, para ver si corresponden al Scope, en cuyo caso
            # las elimina, caso contrario las deja
            heap = self.symbols.get(sym)
            # Una vez creada una entrada en el diccionario la Pila siempre existe, aunque puede estar varia
            if heap is None:
                raise ValueError(
                    "Error Semantico; Entrada en diccionario sin definicion de Pila".format(sym))
                BaseASTNode.add_result(
                    "Error Semantico; Entrada en diccionario sin definicion de Pila".format(sym))
            else:
                same_value_and_scope = True
                while same_value_and_scope:
                    # Tengo que desapilar los variables repetidas
                    value = heap.desapilar()
                    # Si el elemento desapilado no corresponde al scope lo vuelvo a apilar
                    # Asumo que los elementos de la arriba de la Pila son de scopes superiores, por lo tanto cuando encuentro
                    # un elemento con scope diferente salgo
                    if not scope == value.get_scope():
                        heap.apilar(value)
                        same_value_and_scope = False
                    # else:
                       # print('Se elimino variable :' + value.get_name())
                    # Siempre que la Pila este vacia elimino la entrada del diccionario
                    if heap.es_vacia():
                        # Si la Pila esta vacia, porque acabo de eliminar el unico elemento que tenia, puedo
                        # asumir que voy a eliminar una entrada en el diccionario que siempre existe
                        del self.symbols[sym]
                        same_value_and_scope = False

    def get_symbol(self, symbol):
        # Una vez que consulto el elemento, debo tener cuidado de no eliminarlo de la pila
        heap = self.symbols.get(symbol)
        if heap:
            value = heap.desapilar()
            heap.apilar(value)
            return value
        else:
            BaseASTNode.add_result(
                "Error Semantico; Variable {} no fue declarada o no se encuentra dentro del scope".format(symbol))
            raise ValueError(
                "Error Semantico; Variable {} no fue declarada o no se encuentra dentro del scope".format(symbol))

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
                    BaseASTNode.add_result(
                        "Error Semantico; Variable {} no posee su estructura de datos interna con datos".format(symbol))
                    raise ValueError(
                        "Error Semantico; Variable {} no posee su estructura de datos interna con datos".format(symbol))
            else:
                BaseASTNode.add_result(
                    "Error Semantico; Variable {} no posee su estructura de datos interna asociada".format(symbol))
                raise ValueError(
                    "Error Semantico; Variable {} no posee su estructura de datos interna asociada".format(symbol))
        else:
            BaseASTNode.add_result(
                "Error Semantico; Variable {} no fue declarada".format(symbol))
            raise ValueError(
                "Error Semantico; Variable {} no fue declarada".format(symbol))

    def create_symbol(self, symbol, type, location=None, scope=None):
        # Hay que tener en cuenta si el id es local o no. Una forma de manejar esto es a traves de
        # una pila, es decir, se apila cuando se ingresa a un bloque y se desapila cuando se sale del
        # mismo o se finaliza la operacion.
        # Se crean N pilas, una para cada id, lo primero es chequear si existe o no la misma
        # Debo verificar que para el entorno o scope actual no existe otro identificador con el mismo nombre.
        # Siempre voy a apilar un nuevo elemento o simbolo en la pila
        sb = SymbolsWrapper(symbol, type, None, location, scope)
        # Obtiene la Pila correspondiente del diccinario. El mismo esta indexado por nombre de variable
        heap = self.symbols.get(symbol)
        # Si no existe Pila, la creo
        if heap is None:
            heap = Pila()
            # Inserta nueva Pila "vacia" en el diccionario
            self.symbols[symbol] = heap
        else:
            # Si la Pila existe la obtengo. Solo existe en el caso que ya hubiera una variable denominada igual
            heap = self.symbols[symbol]

        # Siempre apila
        heap.apilar(sb)
