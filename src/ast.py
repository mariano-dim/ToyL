from rply import Token


class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class Identifier():
    def __init__(self, name, symbolTable):
        self.name = name
        self.symbolTable = symbolTable

    def eval(self):
        # Debo chequear que el mismo se encuentre definido
        # symbol = self.symbolTable.getSymbol(self.name)
        return self.name


class BinaryOp():
    def __init__(self, left, right, symbolTable):
        self.left = left
        self.right = right
        self.symbolTable = symbolTable


class Add(BinaryOp):

    def eval(self):
        leftEval = self.left.eval()
        rightEval = self.right.eval()
        leftVal = leftEval
        rightVal = rightEval
        if type(leftEval) is Token:
            tok = leftEval.gettokentype()
            if tok == 'ID':
                leftVal = self.symbolTable.getSymbol(leftEval.getstr())
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())

        return leftVal + rightVal


class Sub(BinaryOp):

    def eval(self):
        leftEval = self.left.eval()
        rightEval = self.right.eval()
        leftVal = leftEval
        rightVal = rightEval
        if type(leftEval) is Token:
            tok = leftEval.gettokentype()
            if tok == 'ID':
                leftVal = self.symbolTable.getSymbol(leftEval.getstr())
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())

        return leftVal - rightVal


class Mul(BinaryOp):

    def eval(self):
        leftEval = self.left.eval()
        rightEval = self.right.eval()
        leftVal = leftEval
        rightVal = rightEval
        if type(leftEval) is Token:
            tok = leftEval.gettokentype()
            if tok == 'ID':
                leftVal = self.symbolTable.getSymbol(leftEval.getstr())
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())

        return leftVal * rightVal


class Div(BinaryOp):

    def eval(self):
        leftEval = self.left.eval()
        rightEval = self.right.eval()
        leftVal = leftEval
        rightVal = rightEval
        if type(leftEval) is Token:
            tok = leftEval.gettokentype()
            if tok == 'ID':
                leftVal = self.symbolTable.getSymbol(leftEval.getstr())
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())

        return leftVal / rightVal


class Bigger(BinaryOp):

    def eval(self):
        leftEval = self.left.eval()
        rightEval = self.right.eval()
        leftVal = leftEval
        rightVal = rightEval
        if type(leftEval) is Token:
            tok = leftEval.gettokentype()
            if tok == 'ID':
                leftVal = self.symbolTable.getSymbol(leftEval.getstr())
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())
        if leftVal > rightVal:
            return True
        else:
            return False


class Smaller(BinaryOp):

    def eval(self):
        leftEval = self.left.eval()
        rightEval = self.right.eval()
        leftVal = leftEval
        rightVal = rightEval
        if type(leftEval) is Token:
            tok = leftEval.gettokentype()
            if tok == 'ID':
                leftVal = self.symbolTable.getSymbol(leftEval.getstr())
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())
        if leftVal < rightVal:
            return True
        else:
            return False


class Equal(BinaryOp):

    def eval(self):
        # Debo chequear que el 'valor' del lado izquierdo concuerde con el valor
        # de la expresion que hay a la derecha
        leftEval = self.left.eval()
        rightEval = self.right.eval()
        leftVal = leftEval
        rightVal = rightEval
        if type(leftEval) is Token:
            tok = leftEval.gettokentype()
            if tok == 'ID':
                leftVal = self.symbolTable.getSymbol(leftEval.getstr())
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())
        if leftVal == rightVal:
            return True
        else:
            return False


class Different(BinaryOp):

    def eval(self):
        leftEval = self.left.eval()
        rightEval = self.right.eval()
        leftVal = leftEval
        rightVal = rightEval
        if type(leftEval) is Token:
            tok = leftEval.gettokentype()
            if tok == 'ID':
                leftVal = self.symbolTable.getSymbol(leftEval.getstr())
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())
        if leftVal != rightVal:
            return True
        else:
            return False


class Assignation(BinaryOp):

    def eval(self):
        rightEval = self.right.eval()
        if type(rightEval) is Token:
            tok = rightEval.gettokentype()
            if tok == 'ID':
                rightVal = self.symbolTable.getSymbol(rightEval.getstr())
        self.symbolTable.setSymbol(self.left.getstr(), rightEval)


class VarDec():
    def __init__(self, name, type, symbolTable):
        self.name = name
        self.type = type
        self.symbolTable = symbolTable

    def eval(self):
        # Todo es un token, siempre debo convertir al valor que me interesa
        self.symbolTable.createSymbol(self.name, self.type)


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
    def __init__(self, value, symbolTable):
        self.value = value
        self.symbolTable = symbolTable

    def eval(self):
        val = self.value.eval()

        if type(val) is Token:
            tok = val.gettokentype()
            if tok == 'ID':
                value = self.symbolTable.getSymbol(val.getstr())
        print(value)