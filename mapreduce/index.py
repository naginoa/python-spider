from functools import reduce


def f(n):
    return n*n


def add(a,b):
    return a*b


#实现reduce将[1,2,3,4,5]变为整数12345
def list2int(a, b):
    return a * 10 + b


#实现map将str转变为int
def str2int(n):
    iterator = [str(i) for i in range(1,9)]
    iterator2 = [i for i in range(1, 9)]
    return dict(zip(iterator, iterator2))[n]


result_f = map(f, [i for i in range(1,9)])
#reduce 不是内置函数需要import
result_add = reduce(add, [i for i in range(1,9)])
result_li2int = reduce(list2int, [i for i in range(1,6)])
result_str2int = map(str2int, [str(i) for i in range(1,8)])
print(list(result_f))
print(result_add)
print(result_li2int)
print(list(result_str2int))