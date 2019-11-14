#!/usr/bin/python3
from interpreter import Interpreter
from myparser import Parser
from lexer import Lexer
from semantic_analyzer import SemanticAnalyzer
from symbol_table import SymbolTreeNode


def main():
    # while True:
    # try:
    # To run under Python3 replace 'raw_input' call
    # with 'input'
    #    text = input('calc> ')
    # except EOFError:
    #    break
    # if not text:
    #    continue
    import sys
    # sys.tracebacklimit = 0
    text = open('file.py', 'r').read()
    ##print(text)
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()

    semantic_analyzer = SemanticAnalyzer()

    try:
        symbol_tree = semantic_analyzer.analyze(tree) # This analyzes for errors but should not
    except Exception as e:
        #print(e)
        import traceback
        traceback.print_exc()
        symbol_tree = None

    print(symbol_tree)

    #interpreter = Interpreter(tree)
    #interpreter.interpret()


if __name__ == '__main__':
    main()
