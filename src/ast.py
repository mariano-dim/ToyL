

class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Identifier():
    def __init__(self, name):
        self.name = name

    def eval(self):
        return self.name

class BinaryOp():
    def __init__(self, left, right, symbolTable):
        self.left = left
        self.right = right
        self.symbolTable = symbolTable


class Add(BinaryOp):

    def eval(self):
        i = self.left.eval()
        d = self.right.eval()
        # Si todos son numeros los sumo, si alguno es identificador obtengo el valor del mismo

        return i + d

class Sub(BinaryOp):

    def eval(self):
        i =  self.left.eval() #- self.right.eval()
        return i

class Mul(BinaryOp):

    def eval(self):
        i = self.left.eval() #* self.right.eval()
        return i

class Div(BinaryOp):

    def eval(self):
        i = self.left.eval() #/ self.right.eval()
        return i

class Bigger(BinaryOp):

    def eval(self):
        if self.left.eval() > self.right.eval():
            return True
        else:
            return False

class Smaller(BinaryOp):

    def eval(self):
        if self.left.eval() < self.right.eval():
            return True
        else:
            return False

class Equal(BinaryOp):

    def eval(self):
        # Debo chequear que el 'valor' del identificador que hay a la izquierda concuerde con el valor
        # de la expresion que hay a la derecha, que tambien puede ser un identificador
        if self.left.eval() == self.right.eval():
            return True
        else:
            return False

class Different(BinaryOp):

    def eval(self):
        if self.left.eval() != self.right.eval():
            return True
        else:
            return False

class Attribution(BinaryOp):

    def eval(self):
        name = self.left.value
        value = self.right.eval()
        self.symbolTable.setSymbol(name, value)

class VarDec():
    def __init__(self, name, symbolTable):
        self.name = name
        self.symbolTable = symbolTable

    def eval(self):
        # Todo es un token, siempre debo convertir al valor que me interesa
        self.symbolTable.createSymbol(self.name)

class Statements():
    def __init__(self, first_child):
        self.children = [first_child]

    def add_child(self, child):
        self.children.append(child)

    def eval(self):
        for i in self.children:
            i.eval()

class If():
    def __init__(self, pred, block):
        self.pred = pred
        self.block = block

    def eval(self):
        cond = self.pred.eval()
        if cond == True:
            # Si no es True no ejecuta el codigo del bloque, obvio no..
            self.block.eval()


class IfElse():
    def __init__(self, pred, block1, block2):
        self.pred = pred
        self.block1 = block1
        self.block2 = block2

    def eval(self):
        cond = self.pred.eval()
        if cond == True:
            self.block1.eval()
        else:
            self.block2.eval()

class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        value = self.value.eval()
        # Si es un Token del tipo idenfificador debo imprimir el valor (Token.value) del valor
        # Si es un identificador, debo ir a buscar su valor a la tabla de simbolos
        print(str(value.value))

