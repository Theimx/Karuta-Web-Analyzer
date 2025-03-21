def fib(n):
    a = 0
    b = 1
    for i in range(1, n + 1):
        if i % 2 != 0:
            c = a + b
            print(a)
            a = c
        else:
            c = a + b
            print(b)
            b = c

fib(30)
