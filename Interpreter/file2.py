def ab(n):
    return n


c = 5
ff = ab(5000)


def fib(n):
    def check(n):
        if n == 0:
            return 0
        if n == 1:
            return 1

    if n == 0 or n == 1:
        return check(n)

    return fib(n - 1) + fib(n - 2)


a = 5
fff = fib(a)


def factorial(n):
    if n == 1:
        return 1

    return n * factorial(n - 1)


a = 100
res = factorial(a)
print(c)
print(ff)
print(ab(2000))
print(res)
print(fff)

v1 = 5
v2 = 10
v3 = 2
v4 = 6

if v1 < v2:
    if v2 >= v3:
        if v4 > v3 and (v3 < v2 or v1 >= v4):
            v5 = 10000
        print(v5)
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
    v3 = 30

print(1 + 2 == 3)
print(1 == 1)
print(1 + 2 == 1)
print(1 + 2 == 2)
print(1 == 1 + 2)
print(1 == 2 + 1)
print(1 == 2)

for i in range(10):
    print(i)

for i in range(10):
    if i == 2:
        break
    print(i)
else:
    print(12000123)
print(max(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
print(min(321, 312, 12, 3, 123, 32, 15, 1325, 13, 5, 34, 2, 41, 4, 12, 3, 1))
while i < 10:
    i = i + 1
    if i == 2:
        continue
    print(i)
    if i == 5:
        break
else:
    print(321123)