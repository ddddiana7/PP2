def generator(n):
    for i in range (n):
        yield i*i

n = int (input("Enter your number: "))

gen = generator(n)

for value in gen:
    print(value )