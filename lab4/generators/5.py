def generator(n):
    while n >= 0:
        yield n
        n -=1

n = int (input("Enter your number: "))
gen = generator (n)
for value in gen:
    print (value)