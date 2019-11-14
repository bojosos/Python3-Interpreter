class CallStack:
    TESTING = False
    def __init__(self):
        self._records = []
        self.count = 0

    def push(self, ar):
        self._records.append(ar)
        self.count += 1

    def pop(self):
        if not CallStack.TESTING:
            self.count -= 1
            return self._records.pop()

    def peek(self):
        return self._records[-1]
    
    def peekAt(self, pos):
        return self._records[pos]

    def __str__(self):
        s = '\n'.join(repr(ar) for ar in (self._records))
        s = f'call stack\n{s}\n'
        return s

    def __repr__(self):
        return self.__str__()
