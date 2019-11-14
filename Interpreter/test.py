#!/usr/bin/python3

import os, sys
from argparse import ArgumentParser
from call_stack import CallStack
from lexer import Lexer
from myparser import Parser
from symbol_table import ScopedSymbolTable, SymbolTable
from interpreter import Interpreter
from semantic_analyzer import SemanticAnalyzer


def block_print():
    if not ('-p' in sys.argv or '--print' in sys.argv):
        sys.stdout = open(os.devnull, 'w')

def enable_print():
    sys.stdout = sys.__stdout__

def cmp(ans, inans):
    if len(ans) != len(inans):
        return False
    #print(inans)
    for k, v in ans.items():
        if ans[k] != inans.get(k):
            return False

    return True

def make_interpreter(src):
    lexer = Lexer(src)
    parser = Parser(lexer)
    tree = parser.parse()
    semantic_analyzer = SemanticAnalyzer()

    try:
        semantic_analyzer.visit(tree)
    except Exception as e:
        print(e)

    interpreter = Interpreter(tree)
    return interpreter

def extract_ans(stack):
    res = {}
    for ar in stack._records:
        for member in ar.members:
            res[member] = ar.members[member]

    return res

def if_with_else_elif():
    block_print()
    src = """
        var1 = 2
        var2 = 3
        var3 = 4
        if var1 == var2:
            var5 = 
    """

def single_condition_if_statement_test():
    block_print()
    src = """
        var1 = 2
        var2 = 3
        if var1 <= var2:
            var3 = 4
            if var3 < 5:
                var5 = 6
    """

    interpreter = make_interpreter(src)
    
    interpreter.interpret()

    ans = { 'var1': 2, 'var2': 3, 'var3': 4, 'var5': 6}
    inans = extract_ans(interpreter.call_stack)

    enable_print()

    if not cmp(ans, inans):
        return (False, ans, inans, src)
    return (True, ans, inans, src)

def order_of_precedence_test():
    block_print()
    src = """
        var1 =   2
        var2 =   3
        var3 =   1.2
        var4 =   var2 / var1
        var5 =   var1 * var2 + var3 + var4 + 2 * (1 * 2 + 1)
    """

    interpreter = make_interpreter(src)
    interpreter.interpret()
    
    ans = { 'var1': 2, 'var2': 3, 'var3': 1.2, 'var4': 1.5, 'var5': 14.7}
    inans = extract_ans(interpreter.call_stack)

    enable_print()

    if not cmp(ans, inans):
        return (False, ans, inans, src)

    return (True, ans, inans, src)

def simple_vars_test():
    block_print()
    src = """
        var1 = 2
        var2 = 3
        var3 = var1 + var2
    """
    
    interpreter = make_interpreter(src)
    interpreter.interpret()

    ans = {'var1': 2, 'var2': 3, 'var3': 5}
    inans = extract_ans(interpreter.call_stack)

    enable_print()

    if not cmp(ans, inans):
        return (False, ans, inans, src)

    return (True, ans, inans, src)

def if_without_else():
    block_print()
    src = """v1 = 5
v2 = 10
v3 = 2
v4 = 6

if v1 < v2:
    if v2 >= v3:
        if v4 > v3 and (v3 < v2 or v1 >= v4):
            v5 = 10000
        if (((v5 == 1000))):
            v6 = 100000
        if 3 == 4:
            v7 = 10
        if 2 != 2:
            v8 = 5
        if 3 - 2 < 0:
            v9 = 1
        if 2 - 3 < 0:
            v10 = 1
            v3 = 100
    v3 = 3
"""
    
    interpreter = make_interpreter(src)
    interpreter.interpret()

    ans = {'v1': 5,'v2': 10,'v3': 3,'v4': 6,'v5': 10000, 'v10': 1}
    print(interpreter.call_stack)
    inans = extract_ans(interpreter.call_stack)

    enable_print()

    if not cmp(ans, inans):
        return (False, ans, inans, src)
    return (True, ans, inans, src)

def main():
    CallStack.TESTING= True
    tests = {
        'Simple expression test': simple_vars_test,
        'Order of precedence test': order_of_precedence_test,
        'Singe condition if statments test': single_condition_if_statement_test,
        'Complex if statement stuff without else and elif': if_without_else
    }

    print('Starting testing sequence. CallStack pop is %s.' % ('disabled' if CallStack.TESTING else 'enabled'))
    
    cnt = 0

    for idx,k in enumerate(tests.items()):
        res = k[1]()
        if not res[0]:
            print(str(idx + 1) + '. ' + k[0] + ' failed!')
            print('Expected: ', res[1])
            print('Received: ', res[2])
            if '--src' in sys.argv:
                print(res[3])
        else:
            print(str(idx + 1) + '. ' + k[0] + ' passed!')
            if '-v' in sys.argv or '--verbose' in sys.argv:
                print('Expected: ', res[1])
                print('Received: ', res[2])
            if '--src' in sys.argv:
                print(res[3])
            cnt += 1

    print('Tests completed with %d/%d passed' % (cnt , len(tests)))

if __name__ == "__main__":
    main()
