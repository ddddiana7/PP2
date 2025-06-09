def unique(a):
    result = []
    for i in a:
        if i not in result:
            result.append(i)
    return result

a = list(map(int, input("Enter an array: "). split()))

unique(a)

print("Unique elements:", unique(a))