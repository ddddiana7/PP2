import functools

def my(lst):
    print(functools.reduce (lambda x, y: x *y, lst))

lst = map(int, list(input().split()))

my(lst)