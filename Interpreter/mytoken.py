from enum import Enum

class TokenType(Enum):
    #Single character tokens
    PLUS             = '+'
    MINUS            = '-'
    MUL              = '*'
    FLOAT_DIV        = '/'
    LPAREN           = '('
    RPAREN           = ')'
    COLON            = ':'
    COMMA            = ','
    LSS              = '<'
    GTR              = '>'
    ASSIGN           = '='

    # multichar tokens
    GEQ              = '>='
    LEQ              = '<='
    EQU              = '=='
    NEQ              = '!='

    # block of reserver words
    REAL             = 'FLOAT'
    INTEGER          = 'INTEGER'
    INTEGER_DIV      = 'INTEGER_DIV'
    IF               = 'IF'
    DEF              = 'DEF'
    AND              = 'AND'
    OR               = 'OR'
    ELSE             = 'ELSE'
    ELIF             = 'ELIF'
    RETURN           = 'RETURN'

    # misc
    EOF              = 'EOF'
    EOL              = 'EOL'
    FUNC_CALL         = 'FUNCCALL'
    INDENT           = 'INDENT'
    REAL_CONST       = 'REAL_CONST'
    INTEGER_CONST    = 'INTEGER_CONST'
    ID               = 'ID'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        #print(self.type)

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
