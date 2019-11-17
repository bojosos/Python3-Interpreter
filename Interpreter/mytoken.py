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
    INTEGER_DIV      = '//'

    # block of reserved words
    IF               = 'if'
    ELSE             = 'else'
    ELIF             = 'elif'
    AND              = 'and'
    OR               = 'or'
    DEF              = 'def'
    RETURN           = 'return'
    WHILE            = 'while'
    FOR              = 'for'
    IN               = 'in'
    RANGE            = 'range'
    ENUMERATE        = 'enumerate'
    CONTINUE         = 'continue'

    # misc
    EOF              = 'EOF'
    EOL              = 'EOL'
    FUNC_CALL        = 'FUNCCALL'
    INDENT           = 'INDENT'
    REAL_CONST       = 'REAL_CONST'
    INTEGER_CONST    = 'INTEGER_CONST'
    ID               = 'ID'
    REAL             = 'FLOAT'
    INTEGER          = 'INTEGER'

class Token(object):
    def __init__(self, type, value, lineno=None, column=None):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.column = column

    def __str__(self):
        return 'Token({type}, {value}, position={lineno}:{column})'.format(
            type=self.type,
            value=repr(self.value),
            lineno=self.lineno,
            column=self.column,
        )

    __repr__ = __str__
