import numbers


class BaseASTNode:
    # Esta lista representa el resultado final del interprete, que se debe mostrar en pantalla
    result = []

    def __init__(self):
        pass

    def eval(self):
        print('type: ' + type(self).__name__)
        self.add_ast_element('type: ' + type(self).__name__)

    @staticmethod
    def desapilar_todo(symbol_table):
        from toyl.parser import scopes
        symbol_table.remove_scope_variables(scopes.tope())

    @staticmethod
    def add_result(value):
        # Todo subresultado agregado debe ser imprimible
        print(value)
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


class GrammarError(BaseASTNode):

    def eval(self):
        return None


class Number(BaseASTNode):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class MinusExpression(BaseASTNode):
    def __init__(self, value, symbol_table):
        self.value = value
        self.symbol_table = symbol_table

    def eval(self):
        value = self.value.eval()
        if Utils.is_id(value):
            value = self.symbol_table.get_symbol(value.get_name()).get_value()
        elif not isinstance(value, numbers.Number):
            BaseASTNode.add_result('Error Semantico; Se esperaba un Identificador o un numero entero')
            raise ValueError('Error Semantico; Se esperaba un Identificador o un numero entero')
        return -value


class String(BaseASTNode):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def print(self):
        return self.value.replace('"', '')


class Identifier(BaseASTNode):
    def __init__(self, name, symbol_table):
        self.name = name
        self.symbol_table = symbol_table

    def eval(self):
        # Debo chequear que el mismo se encuentre definido
        # symbol = self.symbol_table.get_symbol(self.name).get_value()
        return self

    def get_name(self):
        return self.name

    def print(self):
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
            left_val = self.symbol_table.get_symbol(left_eval.get_name()).get_value()
        elif Utils.is_string(left_eval):
            BaseASTNode.add_result('Error Semantico; Error de tipos')
            raise ValueError('Error Semantico; Error de tipos')
        elif isinstance(left_eval, numbers.Number):
            left_val = left_eval

        if Utils.is_id(right_eval):
            right_val = self.symbol_table.get_symbol(right_eval.get_name()).get_value()
        elif Utils.is_string(right_eval):
            BaseASTNode.add_result('Error Semantico; Error de tipos')
            raise ValueError('Error Semantico; Error de tipos')
        elif isinstance(right_eval, numbers.Number):
            right_val = right_eval
        return left_val, right_val


class Add(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        # Solo se pueden sumar valores numericos
        try:
            l_value = int(left_val)
            r_value = int(right_val)
        except ValueError as valueError:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, solo se pueden sumar numeros enteros'.format(valueError))
            raise ValueError('Error Semantico; Error de tipos, solo se pueden sumar numeros enteros'.format(valueError))
        return l_value + r_value

    def print(self):
        return self.eval()


class Sub(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        try:
            l_value = int(left_val)
            r_value = int(right_val)
        except ValueError as valueError:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, solo se pueden restar numeros enteros'.format(valueError))
            raise ValueError(
                'Error Semantico; Error de tipos, solo se pueden restar numeros enteros'.format(valueError))
        return l_value - r_value

    def print(self):
        return self.eval()


class Mul(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        try:
            l_value = int(left_val)
            r_value = int(right_val)
        except ValueError as valueError:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, solo se pueden multiplicar numeros enteros'.format(valueError))
            raise ValueError(
                'Error Semantico; Error de tipos, solo se pueden multiplicar numeros enteros'.format(valueError))
        return l_value * r_value

    def print(self):
        return self.eval()


class Div(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        # + ' index ' + str(p.error.index) + ' '
        # + ' lineno ' + str(p.error.lineno) + ' '
        # + ' type ' + p.error.type + ' '
        # + ' value ' + p.error.value)
        try:
            l_value = int(left_val)
            r_value = int(right_val)
        except ValueError as valueError:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, solo se pueden dividir numeros enteros'.format(valueError))
            raise ValueError(
                'Error Semantico; Error de tipos, solo se pueden dividir numeros enteros'.format(valueError))
        # Chequeo la division por cero
        if int(right_val) == 0:
            BaseASTNode.add_result('Error Semantico; No se puede dividir por cero')
            raise ValueError('Error Semantico; No se puede dividir por cero')

        return l_value / r_value

    def print(self):
        return self.eval()


class Bigger(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        try:
            l_value = int(left_val)
            r_value = int(right_val)
        except ValueError as valueError:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, solo se pueden comparar enteros'.format(valueError))
            raise ValueError('Error Semantico; Error de tipos, solo se pueden comparar enteros'.format(valueError))

        if l_value > r_value:
            return True;
        else:
            return False


class Smaller(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        try:
            l_value = int(left_val)
            r_value = int(right_val)
        except ValueError as valueError:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, solo se pueden comparar enteros'.format(valueError))
            raise ValueError('Error Semantico; Error de tipos, solo se pueden comparar enteros'.format(valueError))

        if l_value < r_value:
            return True;
        else:
            return False


class Equal(BinaryOp, BaseASTNode):

    def eval(self):
        # Debo chequear que el 'valor' del lado izquierdo concuerde con el valor
        # de la expresion que hay a la derecha
        left_val, right_val = self.get_values()
        try:
            l_value = int(left_val)
            r_value = int(right_val)
        except ValueError as valueError:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, solo se pueden comparar enteros'.format(valueError))
            raise ValueError('Error Semantico; Error de tipos, solo se pueden comparar enteros'.format(valueError))

        if l_value == r_value:
            return True;
        else:
            return False


class Different(BinaryOp, BaseASTNode):

    def eval(self):
        left_val, right_val = self.get_values()
        try:
            l_value = int(left_val)
            r_value = int(right_val)
        except ValueError as valueError:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, solo se pueden comparar enteros'.format(valueError))
            raise ValueError('Error Semantico; Error de tipos, solo se pueden comparar enteros'.format(valueError))

        if not l_value == r_value:
            return True;
        else:
            return False


class Statements(BaseASTNode):
    def __init__(self, first_child, symbol_table):
        self.children = [first_child]
        self.symbol_table = symbol_table

    def add_child(self, child):
        self.children.append(child)

    def eval(self):
        for i in self.children:
            i.eval()


class If(BaseASTNode):
    def __init__(self, pred, block, symbol_table):
        self.pred = pred
        self.block = block
        self.symbol_table = symbol_table

    def eval(self):
        cond = self.pred.eval()
        if cond:
            # Si no es True no ejecuta el codigo del bloque, obvio no..
            self.block.eval()


class IfElse(BaseASTNode):
    def __init__(self, pred, block1, block2, symbol_table):
        self.pred = pred
        self.block1 = block1
        self.block2 = block2
        self.symbol_table = symbol_table

    def eval(self):
        cond = self.pred.eval()
        if cond:
            self.block1.eval()
        else:
            self.block2.eval()


class Assignation(BinaryOp, BaseASTNode):

    def eval(self):
        # Solo analizo la parte derecha, ya que la izquierda es un Identificador y solo debo revisar
        # que el mismo este definido o heredado del scope del padre
        right_eval = self.right.eval()
        right_value = None

        # Debo realizar el control de tipos de datos, es decir el valor de la expresion debe
        # corresponderse con el tipo de datos definido para el variable
        # Ademas y aun mas prioritario, debo chequear que la variable existe y esta definida en el scope o es heredada
        # del scope del padre
        # Adicionalmente debo chequear que la variable se puede asignar por tener valor derecho
        name_left_variable = self.symbol_table.get_symbol(self.left).get_name()
        td_var_left = self.symbol_table.get_symbol(self.left).get_type()
        location = self.symbol_table.get_symbol(self.left).get_location()
        td_var_right = None

        if not location == "has_left_value":
            BaseASTNode.add_result(
                'Error Semantico; La variable {} no se puede usar como valor izquierdo. No es asignable'.format(
                    name_left_variable))
            raise ValueError(
                'Error Semantico; La variable {} no se puede usar como valor izquierdo. No es asignable'.format(
                    name_left_variable))

        if Utils.is_id(right_eval):
            right_value = self.symbol_table.get_symbol(right_eval.getstr()).get_value()
            td_var_right = self.symbol_table.get_symbol(right_eval.getstr()).get_type()
        elif Utils.is_string(right_eval):
            right_value = right_eval
            td_var_right = 'string'
        elif isinstance(right_eval, numbers.Number):
            right_value = right_eval
            td_var_right = 'int'

        # Justo antes de setear el valor chequeo que la expresion sea del tipo esperado
        if td_var_left == td_var_right:
            self.symbol_table.set_symbol_value(self.left, right_value)
        else:
            BaseASTNode.add_result(
                'Error Semantico; Error de tipos, se esperaba {}, pero la expresion era del tipo {} '.format(
                    td_var_left, td_var_right))
            raise ValueError(
                "Error Semantico; Error de tipos, se esperaba {}, pero la expresion era del tipo {} ".format(
                    td_var_left, td_var_right))


class VarDec(BaseASTNode):
    def __init__(self, token_name, token_type, symbol_table):
        # Obtengo el valor de cada Token antes de ser procesado
        self.name = token_name
        self.type = token_type
        self.location = 'has_left_value'
        self.symbol_table = symbol_table

    def eval(self):
        from toyl.parser import scopes
        # print('variable: ' + self.name + ' definida en Scope: ' + str(scopes.tope()))
        # BaseASTNode.add_result('Variable {}, definida en Scope: {} '.format(self.name, str(scopes.tope())))
        # To-do es un token, siempre debo convertir al valor que me interesa
        self.symbol_table.create_symbol(self.name, self.type, self.location, scopes.tope())


class While(BaseASTNode):
    def __init__(self, cond, block, symbol_table):
        self.cond = cond
        self.block = block
        self.symbol_table = symbol_table
        self.scope_declared = False

    def eval(self):
        if not self.scope_declared:
            from toyl.parser import scopes
            tope = scopes.tope()
            scopes.apilar(tope + 1)
            # print('Creando scope local: ', tope + 1)
            # BaseASTNode.add_result('Creando scope local: {}'.format(str(tope + 1)))
            self.scope_declared = True

        cond = self.cond.eval()
        if cond:
            # Debo ejecutar las instrucciones del bloque, y entre ellas las definiciones de variables
            # de alguna forma tengo que decirle al bloque se es ejecuta dentro del scope N
            self.block.eval()
            self.eval()
        else:
            # Voy a definir aca la logica para cuando sale del bloque while, es decir  aqui pude identificar
            # El punto de retorno y por ende es un punto correcto para eliminar las variables declaradas dentro del bloque
            # Cuales son las variables declaradas dentro del bloque?
            # Cuando salgo del bloque while reseteo el valor de scope_local a False
            from toyl.parser import scopes
            tope = scopes.tope()
            # print('Eliminando scope: ', tope)
            # BaseASTNode.add_result('Eliminando scope: {}'.format(str(tope)))
            # la eliminacion del Scope implica desapilar todos los elementos de la Pila de varuables
            BaseASTNode.desapilar_todo(self.symbol_table)
            scopes.desapilar()


class DoWhile(BaseASTNode):
    def __init__(self, cond, block, symbol_table):
        self.cond = cond
        self.block = block
        self.firt_time = True
        self.symbol_table = symbol_table

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
        values_list = []
        # Creo una lista con todos los elementos que se deben imprimir
        for elem in self.value.children:
            values_list.append(elem)
        values_list_without_variables = []
        # Creo otra lista a la cual voy a copiar los valores finales a imprimir
        for elem in values_list:
            if Utils.is_id(elem):
                value = self.symbol_table.get_symbol(elem.get_name()).get_value()
                values_list_without_variables.append(str(value))
            else:
                values_list_without_variables.append(str(elem.print()))
        # print(''.join(values_list_without_variables))
        BaseASTNode.add_result('{}'.format(''.join(values_list_without_variables)))


class PrintParams(BaseASTNode):
    def __init__(self, first_child, symbol_table):
        self.symbol_table = symbol_table
        self.children = [first_child]

    def add_child(self, child):
        self.children.append(child)

    def eval(self):
        for i in self.children:
            i.eval()


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

        self.symbol_table.create_symbol(self.id, 'int', 'not_izda')

        step_value = initial_value
        if Utils.is_orden_to(orden):
            while step_value <= final_value:
                self.symbol_table.set_symbol_value(self.id, step_value)
                self.statement_list.eval()
                step_value += 1
        else:
            while step_value >= final_value:
                self.symbol_table.set_symbol_value(self.id, step_value)
                self.statement_list.eval()
                step_value -= 1


class ForList(BaseASTNode):
    def __init__(self, initial_value, orden, final_value):
        self.id = id
        self.initial_value = initial_value
        self.orden = orden
        self.final_value = final_value

    def eval(self):
        # Aca puedo chequear limites u semantica del orden
        # Tambien se puede chequear el scope de las variables
        pass


class Utils:

    @staticmethod
    def is_id(value):
        if type(value) is Identifier:
            return True
        else:
            return False

    @staticmethod
    def is_num(value):
        if isinstance(value, numbers.Number):
            return True
        else:
            return False

    @staticmethod
    def is_string(value):
        if not isinstance(value, numbers.Number):
            return True
        else:
            return False

    @staticmethod
    def is_orden_to(value):
        if value == 'to':
            return True
        else:
            return False

    @staticmethod
    def is_orden_downto(value):
        if value == 'downto':
            return True
        else:
            return False
