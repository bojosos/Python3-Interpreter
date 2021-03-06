from mytoken import TokenType
from visitor import NodeVisitor
from call_stack import CallStack
from symbol_table import SymbolTreeNode
from activation_record import ARType, ActivationRecord
from symbol import VarSymbol, FuncDefSymbol, IfStatementSymbol, Symbol
from error import InterpreterError, ErrorCode
from builtin import Builtins


class Interpreter(NodeVisitor):
    UNIT_TESTING = False

    def __init__(self, tree):
        self.tree = tree
        self.symbol_tree = SymbolTreeNode('program', None, None)
        self.call_stack = CallStack()
        self.cont = False
        self.breaking = False
        self.builtins = Builtins()

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for child in node.children:
            if self.cont or self.breaking:
                break
            if self.call_stack.count != 0:
                break
            self.visit(child)

    def visit_Break(self, node):
        self.breaking = True

    def visit_LoopBlock(self, node):
        for child in node.children:
            if self.cont:
                self.cont = False
                return False
            if self.breaking:
                self.breaking = False
                return True
            if self.call_stack.count != 0:
                break
            self.visit(child)

        return False

    def visit_Continue(self, node):
        self.cont = True

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == TokenType.INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        if node.op.type == TokenType.FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)
        if node.op.type == TokenType.LSS:
            return self.visit(node.left) < self.visit(node.right)
        if node.op.type == TokenType.LEQ:
            return self.visit(node.left) <= self.visit(node.right)
        if node.op.type == TokenType.EQU:
            return self.visit(node.left) == self.visit(node.right)
        if node.op.type == TokenType.NEQ:
            return self.visit(node.left) != self.visit(node.right)
        if node.op.type == TokenType.GTR:
            return self.visit(node.left) > self.visit(node.right)
        if node.op.type == TokenType.GEQ:
            return self.visit(node.left) >= self.visit(node.right)

    def visit_IfStatement(self, node):
        r = self.visit(node.condition)
        if r:
            self.visit(node.exec_block)
        else:
            for el in node.elifs:
                if self.visit(el):
                    break
            else:
                if node.elseObj:
                    self.visit(node.elseObj)

    def visit_ElIf(self, node):
        r = self.visit(node.condition)
        if r:
            self.visit(node.exec_block)
            return True
        return False

    def visit_Else(self, node):
        self.visit(node.exec_block)

    def visit_Condition(self, node):
        res = self.visit(node.exprs[0])
        for expr in range(1, len(node.exprs)):
            if node.exprs[expr][1] == TokenType.AND:
                res = self.visit(node.exprs[expr][0]) and res
            if node.exprs[expr][1] == TokenType.OR:
                res = self.visit(node.exprs[expr][0]) or res

        return res

    def visit_Return(self, node):
        a = self.visit(node.expr)
        ar = ActivationRecord('return', ARType.RETURN, self.call_stack.count + 1)
        ar['return'] = a
        self.call_stack.push(ar)

    def visit_WhileLoop(self, node):
        while self.visit(node.condition):
            if self.visit(node.exec_block):
                break
        else:
            if node.else_exec_block is not None:
                self.visit(node.else_exec_block)

    def visit_ForLoop(self, node):
        if node.end == 'range':
            for i in range(self.visit(node.range[0]), self.visit(node.range[1]), self.visit(node.range[2])):
                self.symbol_tree.insert_var(VarSymbol(self.visit(node.var), i))
                if self.visit(node.exec_block):
                    break
            else:
                if node.else_exec_block is not None:
                    self.visit(node.else_exec_block)

    def visit_FuncDef(self, node):
        self.symbol_tree.insert_child(FuncDefSymbol(node.name, node.params, node.exec_block))

    def visit_FuncCall(self, node):

        if node.name in self.builtins.names:
            self.symbol_tree.insert_child(Symbol(node.name))
            self.symbol_tree = self.symbol_tree.children[-1]

            visited_params = []
            for param in node.params.params:
                visited_params.append(self.visit(param))
            ret = self.builtins.call(node.name, visited_params)

            self.symbol_tree = self.symbol_tree.parent
            return ret

        func = self.symbol_tree.lookup_function(node.name)
        if func:
            self.symbol_tree.insert_child(IfStatementSymbol(''))
            self.symbol_tree = self.symbol_tree.children[-1]

            self.visit(node.params)
            self.visit(func.exec_block)

            self.symbol_tree = self.symbol_tree.parent
            return self.call_stack.pop().members['return']
        else:
            raise Exception('Function definition not found')

    def visit_Params(self, node):
        for i in range(len(node.params)):
            param = node.params[i]
            var_name = self.symbol_tree.lookup_function(node.name).params.params[i].value
            self.symbol_tree.insert_var(VarSymbol(var_name, self.visit(param)))

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type

        if op == TokenType.PLUS:
            return +self.visit(node.expr)
        elif op == TokenType.MINUS:
            return -self.visit(node.expr)

    def visit_Assign(self, node):
        var_name = self.visit(node.left)
        var_value = self.visit(node.right)

        self.symbol_tree.insert_var(VarSymbol(var_name, var_value))

    def visit_Var(self, node):
        var_name = node.value

        var_value = self.symbol_tree.lookup(var_name)

        if var_value is None:
            raise InterpreterError(error_code=ErrorCode.ID_NOT_FOUND)

        return var_value.value

    def visit_VarDecl(self, node):
        return node.name

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''

        return self.visit(tree)
