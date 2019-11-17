
class SymbolTreeNode(object):
    def __init__(self, node_name, parent, symbol):
        self.node_name = node_name
        self.parent = parent
        self.symbol = symbol
        self.children = []
        self.childIdx = 0
        self.members = {}

    def insert_var(self, symbol):
        self.members[symbol.name] = symbol

    def insert_child(self, symbol):
        self.children.append(SymbolTreeNode(symbol.name, self, symbol))
        return len(self.children) - 1

    def lookup_function(self, name):
        if self.symbol is not None and self.symbol.name == name:
            return self.symbol

        var = None
        for func in self.children:
            if func.symbol.name == name:
                var = func.symbol

        if var is not None:
            return var

        if self.parent is not None:
            return self.parent.lookup_function(name)
        return None

    def lookup(self, name):
        var = self.members.get(name)

        if var is not None:
            return var

        if self.parent is not None:
            return self.parent.lookup(name)
        return None
