from rply import Token


class Number():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class Identifier():
    def __init__(self, name, symbol_table):
        self.name = name
        self.symbol_table = symbol_table

    def eval(self):
        # Debo chequear que el mismo se encuentre definido
        # symbol = self.symbol_table.get_symbol(self.name)
        return self.name


class BinaryOp():
    def __init__(self, left, right, symbol_table):
        self.left = left
        self.right = right
        self.symbol_table = symbol_table

    def get_values(self):
        left_eval = self.left.eval()
        right_eval = self.right.eval()
        left_val = None
        right_val = None
        if Utils.is_num(left_eval):
            left_val = left_eval.getstr()
        elif Utils.is_id(left_eval):
            left_val = self.symbol_table.get_symbol(left_eval.getstr())

        if Utils.is_num(right_eval):
            right_val = right_eval.getstr()
        elif Utils.is_id(right_eval):
            right_val = self.symbol_table.get_symbol(right_eval.getstr())
        return left_val, right_val


class Add(BinaryOp):

    def eval(self):
        left_val, right_val = self.get_values()
        return int(left_val) + int(right_val)


class Sub(BinaryOp):

    def eval(self):
        left_val, right_val = self.get_values()
        return int(left_val) - int(right_val)


class Mul(BinaryOp):

    def eval(self):
        left_val, right_val = self.get_values()
        return int(left_val) * int(right_val)


class Div(BinaryOp):

    def eval(self):
        left_val, right_val = self.get_values()
        return int(left_val) / int(right_val)


class Bigger(BinaryOp):

    def eval(self):
        left_val, right_val = self.get_values()
        if int(left_val) > int(right_val):
            return True
        else:
            return False


class Smaller(BinaryOp):

    def eval(self):
        left_val, right_val = self.get_values()
        if int(left_val) < int(right_val):
            return True
        else:
            return False


class Equal(BinaryOp):

    def eval(self):
        # Debo chequear que el 'valor' del lado izquierdo concuerde con el valor
        # de la expresion que hay a la derecha
        left_val, right_val = self.get_values()
        if int(left_val) == int(right_val):
            return True
        else:
            return False


class Different(BinaryOp):

    def eval(self):
        left_val, right_val = self.get_values()
        if not int(left_val) == int(right_val):
            return True
        else:
            return False


class Assignation(BinaryOp):

    def eval(self):
        # Solo analizo la parte derecha, ya que la izquierda es un Identificador y solo debo revisar
        # que el mismo este definido
        right_eval = self.right.eval()
        right_value = None

        if Utils.is_id(right_eval):
            right_value = self.symbol_table.get_symbol(right_eval.getstr())
        elif Utils.is_num(right_eval):
            right_value = right_eval.getstr()
        elif isinstance(right_eval, int):
            right_value = right_eval
        self.symbol_table.set_symbol(self.left.getstr(), right_value)


class VarDec:
    def __init__(self, token_name, token_type, symbol_table):
        # Obtengo el valor de cada Token antes de ser procesado
        self.name = token_name.getstr()
        self.type = token_type.getstr()
        self.symbol_table = symbol_table
        # No es factible definir un Token como indice en un diccionario, a esta altura
        # debo trabajar con los valores directamente

    def eval(self):
        # Todo es un token, siempre debo convertir al valor que me interesa
        self.symbol_table.create_symbol(self.name, self.type)


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
        if cond:
            # Si no es True no ejecuta el codigo del bloque, obvio no..
            self.block.eval()


class IfElse():
    def __init__(self, pred, block1, block2):
        self.pred = pred
        self.block1 = block1
        self.block2 = block2

    def eval(self):
        cond = self.pred.eval()
        if cond:
            self.block1.eval()
        else:
            self.block2.eval()


class Print():
    def __init__(self, value, symbol_table):
        self.value = value
        self.symbol_table = symbol_table

    def eval(self):
        value = self.value.eval()
        if Utils.is_id(value):
            value = self.symbol_table.get_symbol(value.getstr())
        elif Utils.is_num(value):
            value = value.getstr()
        print(value)


class Utils:

    @staticmethod
    def is_id(value):
        if type(value) is Token:
            tok = value.gettokentype()
            if tok == 'ID':
                return True
            else:
                return False

    @staticmethod
    def is_num(value):
        if type(value) is Token:
            tok = value.gettokentype()
            if tok == 'NUMBER':
                return True
            else:
                return False
