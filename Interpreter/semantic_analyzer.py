from visitor import *
from symbol_table import ScopedSymbolTable
from symbol import VarSymbol, IfStatementSymbol


class SemanticAnalyzer(NodeVisitor):
    def __init__(self):
        self.current_scope = None

    def visit_Block(self, node):
        for child in node.children:
            self.visit(child)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        pass

    def visit_IfStatement(self, node):
        self.visit(node.exec_block)
    
    def visit_Params(self, node):
        pass

    def visit_Return(self, node):
        pass

    def visit_Condition(self, node):
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_Assign(self, node):
        var_name = self.visit(node.left)

        var_symbol = self.current_scope.insert(VarSymbol(var_name))
        #if var_symbol is None:
        #    raise NameError(repr(var_name))

        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)

        if var_symbol is None:
            raise NameError('Error: Symbol(identifier) not found %s' % var_name)

    def visit_VarDecl(self, node):
        var_name = node.name

        var_symbol = VarSymbol(var_name)

        self.current_scope.insert(var_symbol)
        #self.symbol_table.insert(var_symbol)

    def visit_Num(self, node):
        #print("Node in visit num", node)
        return node.value

    def visit_NoOp(self, node):
        pass

    def visit_FuncCall(self, node):
        pass

    def visit_FuncDef(self, node):
        self.visit(node.exec_block)

    def visit_Program(self, node):
        global_scope = ScopedSymbolTable(scope_name='global', scope_level=1, enclosing_scope=self.current_scope)
        global_scope._init_builtins()
        self.current_scope = global_scope

        self.visit(node.block)
        self.current_scope = self.current_scope.enclosing_scope

    def analyze(self, tree):
        self.visit(tree)
