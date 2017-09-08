def is_odd(n):
    return n % 2 == 0


#使用filter实现计算素数的埃氏筛法
def init_list():
    n = 1
    while True:
        n += 2
        yield n


def _not_divisible(n):
    return lambda x: x % n > 0


def primes():
    yield 2
    it = init_list()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)


list_odd = filter(is_odd, [1,2,3,4,5])
print(list(list_odd))
for i in primes():
    if i < 1000:
        print(i)