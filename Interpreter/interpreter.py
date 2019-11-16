from mytoken import TokenType
from visitor import NodeVisitor
from call_stack import CallStack
from symbol_table import SymbolTreeNode
from activation_record import ARType, ActivationRecord
from symbol import VarSymbol, FuncDefSymbol, IfStatementSymbol, Symbol
from error import InterpreterError, ErrorCode


class Interpreter(NodeVisitor):
    UNIT_TESTING = False

    def __init__(self, tree):
        self.tree = tree
        self.symbol_tree = SymbolTreeNode('program', None, None)
        self.call_stack = CallStack()
        if Interpreter.UNIT_TESTING:
            self.debug_memory = {}

    def visit_Program(self, node):
        self.visit(node.block)
        print('')

    def visit_Block(self, node):
        for child in node.children:
            if self.call_stack.count != 0:
                break
            self.visit(child)

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
            # self.symbol_tree.insertChild(IfStatementSymbol(node.exec_block))
            # self.symbol_tree = self.symbol_tree.children[-1]

            # Turn out variables in python are scoped to the innermost function, class, module
            # huh who knew

            self.visit(node.exec_block)
            # self.symbol_tree = self.symbol_tree.parent
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
            ar = ActivationRecord('elif', ARType.ELIF, self.call_stack.count + 1)
            self.call_stack.push(ar)
            self.visit(node.exec_block)
            for m in self.call_stack.peek().members:
                del self.symbol_table.symbols[m]
            self.call_stack.pop()
            return True
        return False

    def visit_Else(self, node):
        pass

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
            print('aaa')
            self.visit(node.exec_block)

    def visit_ForLoop(self, node):
        if node.end == 'range':
            for i in range(self.visit(node.range[0]), self.visit(node.range[1]), self.visit(node.range[2])):
                self.symbol_tree.insertVar(VarSymbol(self.visit(node.var), i))
                self.visit(node.exec_block)

    def visit_FuncDef(self, node):
        self.symbol_tree.insertChild(FuncDefSymbol(node.name, node.params, node.exec_block))

    def visit_FuncCall(self, node):

        if node.name == 'print':
            self.symbol_tree.insertChild(Symbol('print'))
            self.symbol_tree = self.symbol_tree.children[-1]
            for par in node.params.params:
                val = self.visit(par)
                if Interpreter.UNIT_TESTING:
                    self.debug_memory[par.value] = val

                print(val)

            self.symbol_tree = self.symbol_tree.parent
            return

        func = self.symbol_tree.lookup_function(node.name)
        if func:
            self.symbol_tree.insertChild(IfStatementSymbol(''))
            self.symbol_tree = self.symbol_tree.children[-1]

            self.visit(node.params)
            self.visit(func.exec_block)

            self.symbol_tree = self.symbol_tree.parent
            # self.symbol_table = self.symbol_table.enclosing_scope
            return self.call_stack.pop().members['return']
        else:
            raise Exception('Function definition not found')

    def visit_Params(self, node):
        # ar = ActivationRecord(node.name, ARType.FUNC, self.call_stack.count + 1)
        for i in range(len(node.params)):
            param = node.params[i]
            var_name = self.symbol_tree.lookup_function(node.name).params.params[i].value
            self.symbol_tree.insertVar(VarSymbol(var_name, self.visit(param)))

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

        print(str(var_name) + ':' + str(var_value))

        # if var_name == 'a':
        #    print()

        self.symbol_tree.insertVar(VarSymbol(var_name, var_value))

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
        print(type(self.tree))
        tree = self.tree
        if tree is None:
            return ''

        return self.visit(tree)
