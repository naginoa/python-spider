from functools import reduce


def f(n):
    return n*n


def add(a,b):
    return a*b


#实现将[1,2,3,4,5]变为整数12345


result_f = map(f, [i for i in range(1,9)])
#reduce 不是内置函数需要import
result_add = reduce(add, [i for i in range(1,9)])
print(list(result_f))
print(result_add)