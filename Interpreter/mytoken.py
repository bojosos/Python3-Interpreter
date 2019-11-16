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

    # block of reserved words
    REAL             = 'FLOAT'
    INTEGER          = 'INTEGER'
    INTEGER_DIV      = 'INTEGER_DIV'
    IF               = 'IF'
    ELSE             = 'ELSE'
    ELIF             = 'ELIF'
    AND              = 'AND'
    OR               = 'OR'
    DEF              = 'DEF'
    RETURN           = 'RETURN'
    WHILE            = 'WHILE'
    FOR              = 'FOR'
    IN               = 'IN'
    RANGE            = 'RANGE'
    ENUMERATE        = 'ENUMERATE'
    CONTINUE         = 'CONTINUE'

    # misc
    EOF              = 'EOF'
    EOL              = 'EOL'
    FUNC_CALL        = 'FUNCCALL'
    INDENT           = 'INDENT'
    REAL_CONST       = 'REAL_CONST'
    INTEGER_CONST    = 'INTEGER_CONST'
    ID               = 'ID'

class Token(object):
    def __init__(self, type, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column
        #print(self.type)

    def __str__(self):
        return 'Token({type}, {value}, position={lineno}:{column})'.format(
            type=self.type,
            value=repr(self.value),
            lineno=self.lineno,
            column=self.column,
        )

    __repr__ = __str__
