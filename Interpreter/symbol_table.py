from symbol import BuiltinTypeSymbol
from enum import Enum


class SymbolTreeNode(object):
    def __init__(self, node_name, parent, symbol):
        self.node_name = node_name
        self.parent = parent
        self.symbol = symbol
        self.children = []

    def insert(self, symbol):
        self.children.append(SymbolTreeNode(symbol.name, self, symbol))
        return len(self.children) - 1

    def dfs_for_print(self):
        import queue as queue
        q = queue.Queue()
        lns = ''
        q.put(self.children)
        lns += 'root: '
        for child in self.children:
            lns += str(child.symbol) + ' '

        line = 0
        while not q.empty():
            lns += '\n'
            line += 1
            lns += str(line) + ': '
            for child in q.get():
                q.put(child.children)
                lns += str(child.symbol) + ' '

        return lns

    def __str__(self):
        return self.dfs_for_print()

    __repr__ = __str__

class ScopeType(Enum):
    FUNCTION = 'FUNCTION'
    GLOBAL = 'GLOBAL'
    DEFAULT = 'DEFAULT'
    RETURN = 'RETURN'


class ScopedSymbolTable(object):
    def __init__(self, scope_name, scope_level, enclosing_scope=None, type=ScopeType.DEFAULT):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self.type = type

    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol('INTEGER'))
        self.insert(BuiltinTypeSymbol('REAL'))

    def __str__(self):

        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'

        lines = ['\n', h1, '=' * len(h1)]

        for header_name, header_value in (
                ('Scope name', self.scope_name),
                ('Scope level', self.scope_level),
                ('Enclosing scope', self.enclosing_scope.scope_name if self.enclosing_scope else None)
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def insert(self, symbol):
        # print('Insert: %s' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        # print('Lookup: %s. (Scope name: %s)' % (name, self.scope_name))
        symbol = self._symbols.get(name)

        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        if self.enclosing_scope is not None:
            scope = self

            #if scope.scope_name == scope.enclosing_scope.scope_name:

            while True:
                if scope.enclosing_scope is not None:
                    scope = self.enclosing_scope
                else:
                    return symbol
                symbol = scope.lookup(name)

                if symbol is not None:
                    return symbol

