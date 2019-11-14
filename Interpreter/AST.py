class AST(object):
    pass

class Program(AST):
    def __init__(self, block):
        self.block = block

class Block(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class VarDecl(AST):
    def __init__(self, name):
        self.name = name

class FuncDef(AST):
    def __init__(self, name, params, exec_block):
        self.name = name
        self.params = params
        self.exec_block = exec_block

class FuncCall(AST):
    def __init__(self, name, params):
        self.name = name
        self.params = params

class Return(AST):
    def __init__(self, expr):
        self.expr = expr

class Params(AST):
    def __init__(self, params, name):
        self.params = params
        self.name = name

class IfStatement(AST):
    def __init__(self, condition, exec_block, elifs, elseObj):
        self.condition = condition
        self.exec_block = exec_block
        self.elifs = elifs
        self.elseObj = elseObj

class Else(AST):
    def __init__(self, exec_block):
        self.exec_block = exec_block

class ElIf(AST):
    def __init__(self, condition, exec_block):
        self.condition = condition
        self.exec_block = exec_block

class Condition(AST):
    def __init__(self, exprs):
        self.exprs = exprs

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass
