from enum import Enum

class ARType(Enum):
    PROGRAM   = 'PROGRAM'
    FUNC      = 'FUNC'
    RETURN    = 'RETURN'

class ActivationRecord:
    def __init__(self, name, type, nesting_level):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.members = {}

    def __setitem__(self, key, value):
        self.members[key] = value

    def __getitem__(self, key):
        return self.members[key]

    def get(self, key):
        return self.members.get(key)

    def __str__(self):
        return str(self.members)

    def __repr__(self):
        return self.__str__()

