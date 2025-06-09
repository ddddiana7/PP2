def myFunc():
    a = input("Enter your string: ")
    b = a.split()
    c = b[:: -1]
    output = " ".join(c)

    print (output)

myFunc()