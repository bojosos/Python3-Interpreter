from mytoken import Token, TokenType
from error import LexerError

RESERVED_KEYWORDS = {}

class Lexer(object):
    def __init__(self, text):
        # client string ut, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

        self.prev_token = None

        self.lineno = 1
        self.column = 1

        self.indent = 0
        self.prev_token = None

    def error(self):
        s = "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(lexeme=self.current_char, lineno=self.lineno,column=self.column)

        raise LexerError(message=s)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def advance(self, cnt=1):
        """Advance the `pos` pointer and set the `current_char` variable."""
        
        for i in range(cnt):
            if self.current_char == '\n':
                self.lineno += 1
                self.column = 0

            self.pos += 1
            if self.pos > len(self.text) - 1:
                self.current_char = None  # Indicates end of input
            else:
                self.current_char = self.text[self.pos]

    def chars(self, cnt):
        if self.pos + cnt > len(self.text) - 1:
            return None
        else:
            return self.text[self.pos:self.pos + cnt]

    def skip_comment(self):
        consC = 1
        while consC < 3:
            if self.current_char == '"':
                consC += 1
            else:
                consC = 1
            self.advance()
        self.advance()

    def skip_whitespace(self):
        #print('starting skip')
        res = 0
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n' or self.current_char == '\r':
                if self.prev_token is not None and self.prev_token.type == TokenType.EOL:
                    res = 0
                self.prev_token = Token(TokenType.EOL, self.current_char)
            if self.current_char == ' ':
                res += 1
            self.advance()

        self.indent = res
            #print('skipped')

    def number(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while(self.current_char is not None and self.current_char.isdigit()):
                result += self.current_char
                self.advance()
            token = Token(TokenType.REAL_CONST, float(result))
        else:
            token = Token(TokenType.INTEGER_CONST, int(result))

        return token

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            #Cprint(self.current_char)
            result += self.current_char
            self.advance()

        if self.current_char == '(' and (self.prev_token is None or self.prev_token.type != TokenType.DEF):
            return Token(TokenType.FUNC_CALL, result)

        token = RESERVED_KEYWORDS.get(result, Token(TokenType.ID, result))
        return token

#
    def get_actual_indent(self):
        res = 0
        while len(self.text) > self.pos + res and self.text[self.pos + res] == ' ':
            #print(self.text[self.pos + res])
            #print('wtf:', self.text[self.pos + res])
            res += 1
        #print(self.text[self.pos+res])
        #print('res:', res)
        return res

    def get_indent(self):
        return self.indent

    def get_next_token(self):
        self.indent = self.get_actual_indent()
        token = self._get_next_token()
        self.prev_token = token
       # print(self.indent)
        return token

    def _get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        #print('char %s' % (self.current_char), end='')
        while self.current_char is not None:

            if self.current_char.isspace():
#                print('Eating space')
                self.skip_whitespace()
                continue
            
            if self.current_char == '"':
                if self.chars(3) == '"""':
                    self.advance(3)
                    self.skip_comment()
                    continue
                else:
                    #String literal
                    pass

            if self.current_char.isdigit():
                return self.number()
        
            if self.chars(6) == 'return':
                self.advance(6)
                return Token(TokenType.RETURN, 'return', self.lineno, self.column)

            if self.chars(3) == 'def':
                self.advance(3)
                return Token(TokenType.DEF, 'def', self.lineno, self.column)

            if self.chars(5) == 'while':
                self.advance(5)
                return Token(TokenType.WHILE, 'while', self.lineno, self.column)

            if self.chars(3) == 'for':
                self.advance(3)
                return Token(TokenType.FOR, 'for', self.lineno, self.column)

            if self.chars(2) == 'in':
                self.advance(2)
                return Token(TokenType.IN, 'in', self.lineno, self.column)

            if self.chars(5) == 'range':
                self.advance(5)
                return Token(TokenType.RANGE, 'range', self.lineno, self.column)

            if self.chars(9) == 'enumerate':
                self.advance(9)
                return Token(TokenType.ENUMERATE, 'enumerate', self.lineno, self.column)

            if self.chars(2) == 'or':
                self.advance(2)
                return Token(TokenType.OR, 'or', self.lineno, self.column)

            if self.chars(3) == 'and':
                self.advance(3)
                return Token(TokenType.AND, 'and', self.lineno, self.column)
        
            if self.chars(2) == 'if':
                self.advance(2)
                return Token(TokenType.IF, 'if', self.lineno, self.column)
            
            if self.chars(2) == '!=':
                self.advance(2)
                return Token(TokenType.NEQ, '!=', self.lineno, self.column)

            if self.chars(2) == '//':
                self.advance(2)
                return Token(TokenType.FLOAT_DIV, '//', self.lineno, self.column)

            if self.chars(4) == 'else':
                self.advance(4)
                return Token(TokenType.ELSE, 'else', self.lineno, self.column)

            if self.chars(4) == 'elif':
                self.advance(4)
                return Token(TokenType.ELIF, 'elif', self.lineno, self.column)

            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            if self.chars(2) == '==':
                self.advance(2)
                return Token(TokenType.EQU, '==', self.lineno, self.column)
            
            if self.chars(2) == '<=':
                self.advance(2)
                return Token(TokenType.LEQ, '<=', self.lineno, self.column)
          
            if self.chars(2) == '>=':
                self.advance(2)
                return Token(TokenType.GEQ, '>=', self.lineno, self.column)
           
            try:
                token_type = TokenType(self.current_char)
            except ValueError:
                self.error()
            else:
                token = Token(token_type, token_type.value, self.lineno, self.column)
                self.advance(1)
                return token
        
        return Token(TokenType.EOF, None, self.lineno, self.column)
