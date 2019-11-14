from AST import *
from mytoken import *


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()
        self.current_indent = 0

    def error(self):
        # pass
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            # print(self.current_token)
            # print('old token: ', self.current_token)
            # self.lexer.indent = self.lexer.get_actual_indent()
            # print('idnent: ' , self.lexer.get_actual_indent())
            self.current_token = self.lexer.get_next_token()
            # print(self.current_token)
        else:
            self.error()

    def get_indent(self):
        return self.lexer.get_indent()

    def factor(self):
        """factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN"""
        token = self.current_token

        if token is None:
            raise Exception("wtf")
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        if token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        if token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            # print('Eating int')
            # print(self.current_token)
            return Num(token)
        if token.type == TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(token)
        if token.type == TokenType.LPAREN:
            # print('LPAREN')
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        if token.type == TokenType.FUNC_CALL:
            node = self.func_call()
            return node

        node = self.variable()
        return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        # print(node)
        while self.current_token.type in (TokenType.MUL, TokenType.INTEGER_DIV, TokenType.FLOAT_DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.INTEGER_DIV:
                self.eat(TokenType.INTEGER_DIV)
            elif token.type == TokenType.FLOAT_DIV:
                self.eat(TokenType.FLOAT_DIV)

            node = BinOp(node, token, self.factor())

        return node

    def expr(self):
        """Arithmetic expression parser / interpreter.

        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
        """
        node = self.term()
        while self.current_token.type in (
        TokenType.PLUS, TokenType.MINUS, TokenType.LSS, TokenType.EQU, TokenType.NEQ, TokenType.GTR, TokenType.GEQ,
        TokenType.LEQ):
            token = self.current_token

            self.eat(token.type)

            node = BinOp(node, token, self.term())
        # print(node)
        return node

    def program(self):

        """
        program: block
        block: statement_list -> the whole program or a function declaration
        statement_list: statement -> the list of commands in a function or program
        statement: empty | assign_statement | compound_statement(do I need this?) -> a command
        empty:
        assign_statement: variable ASSIGN expr
        expr: term ((PLUS | MINUS) term)*
        term: factor ((MUL | FLOATDIV | INTEGERDIV) factor)*
        factor: PLUS factor | MINUS factor | INTEGER_CONST | REAL_CONST | LPAREN expr RPAREN | variable
        variable: ID
        """
        root = Program(self.block(self.get_indent()))
        return root

    def block(self, indent):
        root = Block()

        nodes = self.statement_list(indent)

        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self, indent):
        node = self.statement(indent)
        # print(node)

        result = [node]
        #print('indent: %d, get_indent %d' % (indent, self.get_indent()))
        while indent == self.get_indent() and self.current_token.type != TokenType.EOF:
            result.append(self.statement(self.get_indent()))

        # if self.current_token.type == TokenType.ID:
        # self.error()

        return result

    def ret(self):
        self.eat(TokenType.RETURN)
        expr = self.expr()
        #print(expr)
        return Return(expr)

    def statement(self, indent):

        # print('token in statement: ', self.current_token)
        #        print('current_indent: %d, indent: %d' % (self.current_indent, indent))

        # print(self.get_indent())
        if self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        elif self.current_token.type == TokenType.IF:
            node = self.if_statement(indent)
        elif self.current_token.type == TokenType.DEF:
            node = self.func_def(self.get_indent())
        elif self.current_token.type == TokenType.RETURN:
            # print('Got ret')
            node = self.ret()
        elif self.current_token.type == TokenType.FUNC_CALL:
            node = self.func_call()
        else:
            node = self.empty()
            # print('it\'s else')
        # print('token after statement: ', self.current_token)
        return node

    def func_call(self):
        name = self.current_token.value
        self.eat(TokenType.FUNC_CALL)
        self.eat(TokenType.LPAREN)
        params = self.params(name)
        self.eat(TokenType.RPAREN)

        return FuncCall(name, params)

    def func_def(self, indent):
        self.eat(TokenType.DEF)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)
        params = self.params(name)
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.COLON)
        exec_block = self.block(self.get_indent())

        return FuncDef(name, params, exec_block)

    def params(self, name):
        params = [self.expr()]

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            params.append(self.expr())

        return Params(params, name)

    def if_statement(self, indent):
        self.eat(TokenType.IF)
        # print('We got an if')

        condition = self.condition()

        self.eat(TokenType.COLON)
        exec_block = self.block(self.get_indent())

        elifs = []
        elseObj = None

        while self.current_token.type == TokenType.ELIF:
            self.eat(TokenType.ELIF)
            cond = self.condition()
            self.eat(TokenType.COLON)
            if indent >= self.get_indent():
                self.error()
            ex_block = self.block(self.get_indent())
            elifs.append(ElIf(cond, ex_block))

        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.COLON)

            if indent >= self.get_indent():
                self.error()
            ex_block = self.block(self.get_indent())
            elseObj = Else(ex_block)

        return IfStatement(condition, exec_block, elifs, elseObj)

    def condition(self):
        exprs = [self.expr()]

        token = self.current_token

        while self.current_token.type in (TokenType.AND, TokenType.OR):
            self.eat(self.current_token.type)

            if self.current_token.type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                exprs.append((self.condition(), token.type))
                self.eat(TokenType.RPAREN)
            else:
                exprs.append((self.expr(), token.type))
        # print(exprs)
        return Condition(exprs)

    def assignment_statement(self):
        left = self.variable_decl()
        token = self.current_token
        # print(self.current_token)
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        # left = VarDecl(left, self.get_var_type(right))
        node = Assign(left, token, right)

        return node

    def variable_decl(self):
        # print('VarDecl')
        node = VarDecl(self.current_token.value)
        # print(self.current_token.value)
        self.eat(TokenType.ID)
        return node

    def variable(self):
        # print(self.current_token)
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def empty(self):
        return NoOp()

    def parse(self):
        node = self.program()
        # print(self.current_token)
        if self.current_token.type != TokenType.EOF:
            self.error()
        return node
