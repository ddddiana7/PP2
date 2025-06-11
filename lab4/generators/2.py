def generator(n):
    for i in range (n):
        if i % 2 ==0:
            yield i


n = int (input("Enter your number: "))

gen = generator (n)
for value in gen:
    print(value)