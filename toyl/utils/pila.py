

class Pila:
    """ Representa una pila con operaciones de apilar, desapilar y
        verificar si está vacía. La Pila es agnostica del valor que se apila, ya que no hay comprobacion de tipos"""

    def __init__(self):
        """ Crea una pila vacía. """
        # La pila vacía se representa con una lista vacía
        self.items = []

    def apilar(self, x):
        """ Agrega el elemento x a la pila. """
        # Apilar es agregar al final de la lista.
        self.items.append(x)

    def desapilar(self):
        """ Devuelve el elemento tope y lo elimina de la pila.
            Si la pila está vacía levanta una excepción. """
        try:
            return self.items.pop()
        except IndexError:
            raise ValueError("La pila de simbolos está vacía")


    def tope(self):
        """ Devuelve el elemento tope
            Si la pila está vacía levanta una excepción. """
        try:
            tope =  self.items.pop()
            self.apilar(tope)
            return tope
        except IndexError:
            raise ValueError("La pila de simbolos está vacía")

    def es_vacia(self):
        """ Devuelve True si la lista está vacía, False si no. """
        return self.items == []