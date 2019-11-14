class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__


class IfStatementSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return '<IfStatement{name}>'.format(name=self.name)

    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, value=None):
        super().__init__(name)
        self.value = value

    def __str__(self):
        return '<{name}:{type}'.format(name=self.name, type=self.type)

    __repr__ = __str__


class FuncDefSymbol(Symbol):
    def __init__(self, name, params, exec_block):
        super().__init__(name)
        self.params = params
        self.exec_block = exec_block

    def __str__(self):
        return '<FuncDefSymbol{name}>'.format(name=self.name)

    __repr__ = __str__


class ReturnSymbol(Symbol):
    def __init__(self, val):
        super().__init__('return')
        self.value = val
