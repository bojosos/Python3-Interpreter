#!/usr/bin/python3
from interpreter import Interpreter
from myparser import Parser
from lexer import Lexer


def main():

    text = open('file2.py', 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()

    interpreter = Interpreter(tree)
    interpreter.interpret()


if __name__ == '__main__':
    main()
