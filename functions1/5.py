import itertools

def Myfunc():
    st = input("Enter a string: ")

    op = itertools.permutations(st)

    for o in op:
        print ("". join(o))

Myfunc()

