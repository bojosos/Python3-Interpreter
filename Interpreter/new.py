#!/usr/bin/python3
from interpreter import Interpreter
from myparser import Parser
from lexer import Lexer
from semantic_analyzer import SemanticAnalyzer

def main():
    #while True:
        #try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
        #    text = input('calc> ')
        #except EOFError:
        #    break
        #if not text:
        #    continue
    import sys
    #sys.tracebacklimit = 0
    text = open('file.py', 'r').read()
    ##print(text)
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse() 
    semantic_analyzer = SemanticAnalyzer()
    try:
        semantic_analyzer.visit(tree)
    except Exception as e:
        print(e)

    interpreter = Interpreter(tree)
    interpreter.interpret()

if __name__ == '__main__':
    main()
