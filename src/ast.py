
class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class Identifier():
    def __init__(self, name):
        self.name = name

    def eval(self):
        return self.name


class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOp):
    def eval(self):
        i = self.left.eval() + self.right.eval()
        return i


class Sub(BinaryOp):
    def eval(self):
        i = i = self.left.eval() - self.right.eval()
        return i


class Mul(BinaryOp):
    def eval(self):
        i = i = self.left.eval() * self.right.eval()
        return i


class Div(BinaryOp):
    def eval(self):
        i = i = self.left.eval() / self.right.eval()
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
        print('Attribution')
        # identifier = self.module.get_global(self.left.value)
        # value = self.right.eval()
        # self.builder.store(value, identifier)


class VarDec():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


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
        print('Evaluando IF')
        # Evalua el bloque de instrucciones
        self.block.eval()


class IfElse():
    def __init__(self, pred, block1, block2):
        self.pred = pred
        self.block1 = block1
        self.block2 = block2

    def eval(self):
        cond = self.pred.eval()
        print(cond)
        self.block1.eval()

class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        value = self.value.eval()

