def squares(a, b):
    for i in range (a, b):
        yield i*i

a = int(input("Enter your first number: "))
b = int(input("Enter your second number: "))

gen = squares (a, b)

for value in gen:
    print (value)