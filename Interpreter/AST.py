from mytoken import TokenType, Token


class AST(object):
    pass


class Program(AST):
    def __init__(self, block):
        self.block = block


class Block(AST):
    def __init__(self):
        self.children = []


class Continue(AST):
    pass


class LoopBlock(Block):
    pass


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


class WhileLoop(AST):
    def __init__(self, condition, exec_block, else_exec_block):
        self.condition = condition
        self.exec_block = exec_block
        self.else_exec_block = else_exec_block


class Break(AST):
    pass


class ForLoop(AST):
    def __init__(self, var, end, range, exec_block, else_exec_block):
        self.var = var
        self.end = end
        self.exec_block = exec_block
        self.else_exec_block = else_exec_block
        if len(range) == 1:
            self.range = [Num(0), range[0], Num(1)]
        elif len(range) == 2:
            self.range = [range[0], range[1], Num(1)]
        elif len(range) == 3:
            self.range = range


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
    def __init__(self, value):
        self.value = value


class NoOp(AST):
    pass
