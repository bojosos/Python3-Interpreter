#!/usr/bin/python3

import os
import sys
import io
from lexer import Lexer
from myparser import Parser
from interpreter import Interpreter
import time

Timing = {}


def block_print():
    if not ('-p' in sys.argv or '--print' in sys.argv):
        sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def make_interpreter(src):
    lexer = Lexer(src)
    parser = Parser(lexer)
    tree = parser.parse()

    interpreter = Interpreter(tree)
    return interpreter


def make_test(src, name):
    stdout = sys.stdout
    sys.stdout = io.StringIO()

    timer = [0, 0]

    start = time.time()
    interpreter = make_interpreter(src)
    interpreter.interpret()
    timer[0] = time.time() - start

    out1 = sys.stdout.getvalue()
    sys.stdout = stdout

    stdout = sys.stdout
    sys.stdout = io.StringIO()

    start = time.time()
    exec(src, {})
    timer[1] = time.time() - start

    Timing[name] = timer

    out2 = sys.stdout.getvalue()
    sys.stdout = stdout

    if out1 == out2:
        return True, out1, out2, src
    return False, out1, out2, src


def single_condition_if_statement_test():
    src = \
"""
var1 = 2
var2 = 3
if var1 <= var2:
    var3 = 4
    print(var3)
    if var3 < 5:
        var5 = 6
        print(var5)
        
print(var1)
print(var2)
"""
    return make_test(src, 'single_condition_if_statement_test')

def function_test():
    src = \
"""
def fib(n):
    def check(n):
        if n == 0:
            return 0
        if n == 1:
            return 1

    if n == 0 or n == 1:
        return check(n)

    return fib(n - 1) + fib(n - 2)

def factorial(n):
    if n == 1:
        return 1

    return n * factorial(n - 1)
print(fib(10+factorial(3))+factorial(10-fib(3)))
"""
    return make_test(src, 'function_test')


def order_of_precedence_test():
    src = \
"""
var1 =   2
var2 =   3
var3 =   1.2
var4 =   var2 / var1
var5 =   var1 * var2 + var3 + var4 + 2 * (1 * 2 + 1)
print(var1)
print(var2)
print(var3)
print(var4)
print(var5)
"""

    return make_test(src, 'order_of_precedence_test')


def simple_vars_test():
    src = \
"""
var1 = 2
var2 = 3
var3 = var1 + var2
print(var1)
print(var2)
print(var3)
"""
    return make_test(src, 'simple_vars_test')


def if_with_else():
    src = \
"""
v1=2
v3=3
if v1 == v3:
    print(123)
elif v1 == 2:
    print(321)
else:
    print(1111)
"""
    return make_test(src, 'if_with_else')


def loop_test():
    src = \
"""
for i in range(10):
    if i == 5:
        continue
    print(i)
else:
    print(123123123)
i = 0
while i < 10:
    i = i + 1
    if i == 2:
        continue
    print(i)
    if i == 5:
        break
else:
    print(321123)
"""
    return make_test(src, 'loop_test')


def if_without_else():
    src = """
v1 = 5
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

print(v1)
print(v2)
print(v3)
print(v4)
print(v5)
print(v10)
"""
    return make_test(src, 'if_without_else')


def full_test():
    src = open('full_test.py', 'r').read()

    return make_test(src, 'full_test')


def main():
    run_all()


def run_all():
    tests = {
        'Simple expression test': simple_vars_test,
        'Order of precedence test': order_of_precedence_test,
        'Singe condition if statements test': single_condition_if_statement_test,
        'Complex if statement stuff without else and elif': if_without_else,
        'If with else and elif': if_with_else,
        'Testing loops with continue and else': loop_test,
        'Function test': function_test,
        'Test that tests everything': full_test
    }

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    print(bcolors.HEADER + 'Starting testing sequence!')

    cnt = 0

    for idx, k in enumerate(tests.items()):
        try:
            res = k[1]()
            suc = True
        except Exception as e:
            enable_print()
            print(e)
            print(bcolors.FAIL + bcolors.BOLD + 'Exception in test ', k[0])
            res = [False]

        if not res[0]:
            print(bcolors.FAIL + str(idx + 1) + '. ' + k[0] + ' failed!')
            if len(res) > 1 and ('-v' in sys.argv or '--verbose' in sys.argv):
                print('Expected: ', res[1])
                print('Received: ', res[2])
            if '--src' in sys.argv:
                print(res[3])
        else:
            if '-t' in sys.argv or '--timing' in sys.argv:
                print(bcolors.OKBLUE + str(idx + 1) + '. ' + k[0] +
                      ' passed! Python: %f, You: %f' % (Timing[k[1].__name__][1], Timing[k[1].__name__][0]))
            print(bcolors.OKBLUE + str(idx + 1) + '. ' + k[0] + ' passed!')
            if '-v' in sys.argv or '--verbose' in sys.argv:
                print('Expected: ', res[1])
                print('Received: ', res[2])
            if '--src' in sys.argv:
                print(res[3])
            cnt += 1
    if cnt == len(tests):
        color = bcolors.HEADER
    else:
        color = bcolors.FAIL
    if '-t' in sys.argv or '--timing' in sys.argv:
        python = 0
        me = 0
        for t in Timing:
            me += Timing[t][0]
            python += Timing[t][1]
        print('%sTests completed with %d/%d passed! Python: %f, You: %f' % (color, cnt, len(tests), python, me))
    else:
        print('%sTests completed with %d/%d passed!%s' % (color, cnt, len(tests), bcolors.ENDC))


if __name__ == "__main__":
    main()
