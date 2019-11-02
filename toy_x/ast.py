from rply import Token


class BaseASTNode:
    # Esta lista representa el resultado final del interprete, que se debe mostrar en pantalla
    result = []

    def __init__(self):
        pass

    @staticmethod
    def add_result(value):
        # Todo subresultado agregado debe ser imprimible
        BaseASTNode.result.append(value)

    @staticmethod
    def clean_result():
        # Todo subresultado agregado debe ser imprimible
        BaseASTNode.result.clear()

    @staticmethod
    def get_result():
        return BaseASTNode.result


class Empty(BaseASTNode):

    def eval(self):
        return None


class Number(BaseASTNode):
    def __init__(self, value):
        self.value = value

    def eval(self):
        if Utils.is_num(self.value):
            return int(self.value.getstr())
        else:
            raise ValueError('Error de tipo numerico')

class MinusExpression(BaseASTNode):
    def __init__(self, value, symbol_table):
        self.value = value
        self.symbol_table = symbol_table

    def eval(self):
        value = self.value.eval()
        if Utils.is_id(value):
            value = self.symbol_table.get_symbol(value.getstr()).get_value()
        elif not isinstance(value, int):
            raise ValueError('Se esperaba un Identificador o un numero entero')
        return -value

class String(BaseASTNode):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class Identifier(BaseASTNode):
    def __init__(self, name, symbol_table):
        self.name = name
        self.symbol_table = symbol_table

    def eval(self):
        # Debo chequear que el mismo se encuentre definido
        # symbol = self.symbol_table.get_symbol(self.name).get_value()
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
        if Utils.is_id(left_eval):
            left_val = self.symbol_table.get_symbol(left_eval.getstr()).get_value()
        elif Utils.is_string(left_eval):
            raise ValueError('Error de tipos')
        elif isinstance(left_eval, int):
            left_val = left_eval

        if Utils.is_id(right_eval):
            right_val = self.symbol_table.get_symbol(right_eval.getstr()).get_value()
        elif Utils.is_string(right_eval):
            BaseASTNode.add_result('Error de tipos')
            raise ValueError('Error de tipos')
        elif isinstance(right_eval, int):
            right_val = right_eval
        return left_val, right_val


class Add(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        return int(left_val) + int(right_val)


class Sub(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        return int(left_val) - int(right_val)


class Mul(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        return int(left_val) * int(right_val)


class Div(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        return int(left_val) / int(right_val)


class Bigger(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        if int(left_val) > int(right_val):
            return True
        else:
            return False


class Smaller(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        if int(left_val) < int(right_val):
            return True
        else:
            return False


class Equal(BinaryOp, BaseASTNode):

    def eval(self):
        # Debo chequear que el 'valor' del lado izquierdo concuerde con el valor
        # de la expresion que hay a la derecha
        left_val, right_val = self.get_values()
        if int(left_val) == int(right_val):
            return True
        else:
            return False


class Different(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        if not int(left_val) == int(right_val):
            return True
        else:
            return False


class Assignation(BinaryOp, BaseASTNode):

    def eval(self):
        # Solo analizo la parte derecha, ya que la izquierda es un Identificador y solo debo revisar
        # que el mismo este definido
        right_eval = self.right.eval()
        right_value = None

        # Debo realizar el control de tipos de datos, es decir el valor de la expresion debe
        # corresponderse con el tipo de datos definido para el variable
        td_var_left = self.symbol_table.get_symbol(self.left.getstr()).get_type()
        td_var_right = None

        if Utils.is_id(right_eval):
            right_value = self.symbol_table.get_symbol(right_eval.getstr()).get_value()
            td_var_right = self.symbol_table.get_symbol(right_eval.getstr()).get_type()
        elif Utils.is_num(right_eval):
            right_value = right_eval.getstr()
            td_var_right = 'int'
        elif Utils.is_string(right_eval):
            right_value = right_eval.getstr()
            td_var_right = 'string'
        elif isinstance(right_eval, int):
            right_value = right_eval
            td_var_right = 'int'

        # Justo antes de setear el valor chequeo que la expresion sea del tipo esperado
        if td_var_left == td_var_right:
            self.symbol_table.set_symbol_value(self.left.getstr(), right_value)
        else:
            BaseASTNode.add_result(
                'Error de tipos, se esperaba {}, pero la expresion era del tipo {} '.format(td_var_left, td_var_right))
            raise ValueError(
                "Error de tipos, se esperaba {}, pero la expresion era del tipo {} ".format(td_var_left, td_var_right))


class VarDec(BaseASTNode):
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


class Statements(BaseASTNode):
    def __init__(self, first_child):
        self.children = [first_child]

    def add_child(self, child):
        self.children.append(child)

    def eval(self):
        for i in self.children:
            i.eval()


class If(BaseASTNode):
    def __init__(self, pred, block):
        self.pred = pred
        self.block = block

    def eval(self):
        cond = self.pred.eval()
        if cond:
            # Si no es True no ejecuta el codigo del bloque, obvio no..
            self.block.eval()


class IfElse(BaseASTNode):
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


class While(BaseASTNode):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def eval(self):
        cond = self.cond.eval()
        if cond:
            self.block.eval()
            self.eval()


class DoWhile(BaseASTNode):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block
        self.firt_time = True

    def eval(self):
        if self.firt_time:
            self.firt_time = False
            # Primero ejecuto y despues pregunto
            self.block.eval()
            cond = self.cond.eval()
            if cond:
                self.eval()
        else:
            cond = self.cond.eval()
            if cond:
                self.block.eval()
                self.eval()


class Print(BaseASTNode):
    def __init__(self, value, symbol_table):
        self.value = value
        self.symbol_table = symbol_table

    def eval(self):
        value = self.value.eval()
        if Utils.is_id(value):
            value = self.symbol_table.get_symbol(value.getstr()).get_value()
        elif Utils.is_string(value):
            value = value.getstr()

        BaseASTNode.add_result(value)
        print(value)


class ForLoop(BaseASTNode):
    def __init__(self, id, for_list, statement_list, symbol_table):
        self.id = id
        self.for_list = for_list
        self.statement_list = statement_list
        self.symbol_table = symbol_table

    def eval(self):
        initial_value = self.for_list.initial_value.eval()
        final_value = self.for_list.final_value.eval()
        orden = self.for_list.orden

        self.symbol_table.create_symbol(self.id.getstr(), 'int', 'not_izda')

        step_value = initial_value
        if Utils.is_orden_to(orden):
            while step_value <= final_value:
                self.symbol_table.set_symbol_value(self.id.getstr(), step_value)
                self.statement_list.eval()
                step_value += 1
        else:
            while step_value >= final_value:
                self.symbol_table.set_symbol_value(self.id.getstr(), step_value)
                self.statement_list.eval()
                step_value -= 1
        pass


class ForList(BaseASTNode):
    def __init__(self, initial_value, orden, final_value):
        self.id = id
        self.initial_value = initial_value
        self.orden = orden
        self.final_value = final_value

    def eval(self):
        # Aca puedo chequear limites u semantica del orden
        pass


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
            if tok == 'NUMBER_TYPE':
                return True
            else:
                return False

    @staticmethod
    def is_string(value):
        if type(value) is Token:
            tok = value.gettokentype()
            if tok == 'STRING_TYPE':
                return True
            else:
                return False

    @staticmethod
    def is_orden_to(value):
        if type(value) is Token:
            tok = value.gettokentype()
            if tok == 'TO':
                return True
            else:
                return False

    @staticmethod
    def is_orden_downto(value):
        if type(value) is Token:
            tok = value.gettokentype()
            if tok == 'DOWNTO':
                return True
            else:
                return False
