from mytoken import Token, TokenType
from error import LexerError


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

        self.prev_token = None

        self.lineno = 1
        self.column = 1

        self.indent = 0
        self.prev_token = None

    def error(self):
        s = "Lexer error on '{lexeme}' line: {lineno} column: {column}".format(
            lexeme=self.current_char, lineno=self.lineno, column=self.column)

        raise LexerError(message=s)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def advance(self, cnt=1):
        for i in range(cnt):
            if self.current_char == '\n':
                self.lineno += 1
                self.column = 0

            self.pos += 1
            if self.pos > len(self.text) - 1:
                self.current_char = None
            else:
                self.current_char = self.text[self.pos]

    def skip_comment(self):
        while self.chars(3) != '"""':
            self.advance()
        self.advance()

    def skip_whitespace(self):
        res = 0
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n' or self.current_char == '\r':
                if self.prev_token is not None and self.prev_token.type == TokenType.EOL:
                    res = 0
                self.prev_token = Token(TokenType.EOL, self.current_char, self.lineno, self.column)
            if self.current_char == ' ':
                res += 1
            self.advance()

        self.indent = res

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            token = Token(TokenType.REAL_CONST, float(result))
        else:
            token = Token(TokenType.INTEGER_CONST, int(result))

        return token

    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if self.current_char == '(' and (self.prev_token is None or self.prev_token.type != TokenType.DEF):
            return Token(TokenType.FUNC_CALL, result, self.lineno, self.column)

        token = Token(TokenType.ID, result, self.lineno, self.column)
        return token

#
    def get_actual_indent(self):
        res = 0
        while len(self.text) > self.pos + res and self.text[self.pos + res] == ' ':
            res += 1
        return res

    def get_indent(self):
        return self.indent

    def get_next_token(self):
        self.indent = self.get_actual_indent()
        token = self._get_next_token()
        self.prev_token = token
        return token

    def string(self):
        pass

    def _get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '"':
                if self.chars(3) == '"""':
                    self.advance(3)
                    self.skip_comment()
                    continue
                else:
                    return self.string()

            if self.current_char.isdigit():
                return self.number()

            # A long token: return, for, while, def etc
            s = False
            for i in TokenType:
                if i == TokenType.GEQ or s:
                    s = True
                    for j in range(len(i.value)):
                        if self.text[self.pos + j] != i.value[j]:
                            break
                    else:
                        self.advance(len(i.value))
                        return Token(i, i.value, self.lineno, self.column)
                if i == TokenType.BREAK:
                    break

            # A function or variable name
            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()

            # Single char token
            try:
                token_type = TokenType(self.current_char)
            except ValueError:
                self.error()
            else:
                token = Token(token_type, token_type.value, self.lineno, self.column)
                self.advance(1)
                return token
        
        return Token(TokenType.EOF, None, self.lineno, self.column)
