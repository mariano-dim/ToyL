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
        return self.value


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
        if Utils.is_num(left_eval):
            left_val = left_eval.getstr()
        elif Utils.is_id(left_eval):
            left_val = self.symbol_table.get_symbol(left_eval.getstr()).get_value()
        elif Utils.is_string(left_eval):
            raise ValueError('Error de tipos')
        elif isinstance(left_eval, int):
            left_val = left_eval

        if Utils.is_num(right_eval):
            right_val = right_eval.getstr()
        elif Utils.is_id(right_eval):
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


class ForLoop(BaseASTNode):
    def __init__(self, id, left_expr, right_expr, block, symbol_table):
        self.id = id
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.block = block
        self.symbol_table = symbol_table
        self.left_val = None
        self.right_val = None
        self.declare_and_set_right_variable()

    def declare_and_set_right_variable(self):

        # Obtengo el valor izquierdo y lo registro como tal
        self.symbol_table.create_symbol(self.id.getstr(), 'int')
        # Obtengo el valor del token de la primera expresion, solo admito numeros
        left_value = self.left_expr.eval()
        if Utils.is_num(left_value):
            self.left_val = int(left_value.getstr())
        else:
            raise ValueError('Error de tipos en ForLoop, expresion left no es un numero')
        self.symbol_table.set_symbol_value(self.id.getstr(), self.left_val)
        # Obtengo el valor derecho
        right_value = self.right_expr.eval()
        if Utils.is_num(right_value):
            self.right_val = int(right_value.getstr())
        else:
            raise ValueError('Error de tipos en ForLoop, expresion right no es un numero')

    def eval(self):
        # En el caso del forLoop la variable asignada a la iteracion es local, por lo tanto
        # no es necesario chequear que exista en el entorno. Cuando se salga del bucle la misma se elimina
        # Por otro lado es importante considerarla dentro del bloque
        # Cada vez que defino una nueva variable, tengo que considerar el scope de la misma
        # En este caso estoy declarando una variable sin lado izquierdo, ya que a la misma no se le
        # puede cambiar el valor una vez definida
        # El tipo de datos de las variables de LoopFor es numerico
        # Por otro lado, a diferencia del caso de DoWhile o While, donde se modifica el valor
        # del loop a traves de explicitas modificaciones de variables dentro del loop, aqui
        # no es factible hacer lo mismo y es necesario decrementar el valor directamente
        # La expresion de la izquieza la cambio yo
        # El valor izquierdo lo deb buscar en la tabla de variables, y no en la expresion
        # La expresion de la derecha es INMUTABLE, no debe cambiar
        # El valor de la variable lo tengo en la recursion, pero lo debo registrar para que
        # cualquier uso u operacion dentro del scope tenga el valor correcto
        # Lo puedo resolver mas eficientemente sin recursion, a traves de un bucle y de paso me olvido del
        # problema de los parametros de eval()
        paso = self.left_val
        while paso < self.right_val:
            self.block.eval()
            paso += 1
            self.symbol_table.set_symbol(self.id.getstr(), paso)


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
        elif Utils.is_num(value):
            value = value.getstr()
        BaseASTNode.add_result(value)
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
